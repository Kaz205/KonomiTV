-- upgrade --
CREATE TABLE IF NOT EXISTS "channel" (
    "id" TEXT NOT NULL  PRIMARY KEY,
    "service_id" INT NOT NULL,
    "network_id" INT NOT NULL,
    "channel_id" TEXT NOT NULL,
    "channel_number" TEXT NOT NULL,
    "channel_name" TEXT NOT NULL,
    "channel_type" TEXT NOT NULL,
    "channel_force" INT,
    "is_subchannel" INT NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSON NOT NULL
);