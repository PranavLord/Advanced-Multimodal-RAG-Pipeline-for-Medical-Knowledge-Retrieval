from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(BaseSettings):

    # ==========================================================
    # API Keys
    # ==========================================================

    GOOGLE_API_KEY: str
    GROQ_API_KEY: str
    COHERE_API_KEY: str
    OPENROUTER_API_KEY: str

    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str

    HF_TOKEN: str | None = None

    # ==========================================================
    # LLM Provider
    # ==========================================================

    LLM_PROVIDER: str = "auto"

    # ==========================================================
    # Gemini
    # ==========================================================

    GEMINI_MODEL: str = "gemini-3.6-flash"
    GEMINI_TEMPERATURE: float = 0.2
    GEMINI_TOP_P: float = 0.95
    GEMINI_MAX_OUTPUT_TOKENS: int = 8192

    # ==========================================================
    # Groq
    # ==========================================================

    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_TEMPERATURE: float = 0.2
    GROQ_TOP_P: float = 0.95
    GROQ_MAX_OUTPUT_TOKENS: int = 8192

    # ==========================================================
    # Cohere
    # ==========================================================

    COHERE_MODEL: str = "command-a-03-2025"
    COHERE_TEMPERATURE: float = 0.2
    COHERE_TOP_P: float = 0.95
    COHERE_MAX_OUTPUT_TOKENS: int = 8192

    # ==========================================================
    # OpenRouter
    # ==========================================================

    OPENROUTER_MODEL: str = "openrouter/free"
    OPENROUTER_TEMPERATURE: float = 0.2
    OPENROUTER_TOP_P: float = 0.95
    OPENROUTER_MAX_OUTPUT_TOKENS: int = 8192

    # ==========================================================
    # Environment Configuration
    # ==========================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()