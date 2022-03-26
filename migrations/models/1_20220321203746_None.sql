-- upgrade --
CREATE TABLE IF NOT EXISTS "word" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "word" VARCHAR(128) NOT NULL UNIQUE,
    "rate" DECIMAL(16,10)
);
CREATE INDEX IF NOT EXISTS "idx_word_rate_013847" ON "word" ("rate");
COMMENT ON TABLE "word" IS 'Basic mapper for word table.';
CREATE TABLE IF NOT EXISTS "translation" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "translation" VARCHAR(128) NOT NULL,
    "word_id" UUID NOT NULL REFERENCES "word" ("id") ON DELETE CASCADE
);
CREATE  INDEX IF NOT EXISTS "idx_translation_word_id_553829" ON "translation" ("word_id", "translation");
COMMENT ON TABLE "translation" IS 'Basic mapper for translation to target language.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
