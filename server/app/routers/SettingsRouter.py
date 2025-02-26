
from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import status

from app.config import ClientSettings
from app.config import Config
from app.config import SaveConfig
from app.config import ServerSettings
from app.models import User
from app.routers.UsersRouter import GetCurrentAdminUser
from app.routers.UsersRouter import GetCurrentUser


# ルーター
router = APIRouter(
    tags = ['Settings'],
    prefix = '/api/settings',
)


@router.get(
    '/client',
    summary = 'クライアント設定取得 API',
    response_description = 'ログイン中のユーザーアカウントのクライアント設定。',
    response_model = ClientSettings,
)
async def ClientSettingsAPI(
    current_user: User = Depends(GetCurrentUser),
):
    """
    現在ログイン中のユーザーアカウントのクライアント設定を取得する。<br>
    JWT エンコードされたアクセストークンがリクエストの Authorization: Bearer に設定されていないとアクセスできない。
    """
    return current_user.client_settings


@router.put(
    '/client',
    summary = 'クライアント設定更新 API',
    status_code = status.HTTP_204_NO_CONTENT,
)
async def ClientSettingsUpdateAPI(
    client_settings: ClientSettings = Body(..., description='更新するクライアント設定のデータ。'),
    current_user: User = Depends(GetCurrentUser),
):
    """
    現在ログイン中のユーザーアカウントのクライアント設定を更新する。<br>
    JWT エンコードされたアクセストークンがリクエストの Authorization: Bearer に設定されていないとアクセスできない。
    """

    # dict に変換してから入れる
    ## Pydantic モデルのままだと JSON にシリアライズできないので怒られる
    current_user.client_settings = dict(client_settings)

    # レコードを保存する
    await current_user.save()


@router.get(
    '/server',
    summary = 'サーバー設定取得 API',
    response_description = '現在稼働中の KonomiTV サーバーのサーバー設定。',
    response_model = ServerSettings,
)
async def ServerSettingsAPI(
    current_user: User = Depends(GetCurrentAdminUser),
):
    """
    現在稼働中の KonomiTV サーバーのサーバー設定を取得する。<br>
    Docker 環境では、パス指定の項目は Docker 環境向けの Prefix (/host-rootfs) が付与された状態で返される。<br>

    JWT エンコードされたアクセストークンがリクエストの Authorization: Bearer に設定されていて、かつ管理者アカウントでないとアクセスできない。
    """

    return Config()


@router.put(
    '/server',
    summary = 'サーバー設定更新 API',
    status_code = status.HTTP_204_NO_CONTENT,
)
async def ServerSettingsUpdateAPI(
    server_settings: ServerSettings = Body(..., description='更新するサーバー設定のデータ。'),
    current_user: User = Depends(GetCurrentAdminUser),
):
    """
    現在稼働中の KonomiTV サーバーのサーバー設定を更新する。<br>
    Docker 環境では、パス指定の項目には Docker 環境向けの Prefix (/host-rootfs) を付与した状態でリクエストする必要がある。<br>
    Pydantic のカスタムバリデーターの実装の都合上、バリデーション処理中はメインスレッドが数秒間ブロッキングされることがあるので注意。<br>

    JWT エンコードされたアクセストークンがリクエストの Authorization: Bearer に設定されていて、かつ管理者アカウントでないとアクセスできない。
    """

    # バリデーションが完了したサーバー設定を config.yaml に保存する
    SaveConfig(server_settings)
