from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Water Plant Digital Twin API"
    version: str = "1.0.0"
    model_base_path: str = "models"
    data_base_path: str = "data"
    rw_scaler_file: str = "rw_classifier_scaler.pkl"
    rw_classifier_file: str = "rw_classifier.pkl"
    tw_scaler_file: str = "tw_scaler.pkl"
    tw_predictor_file: str = "tw_predictor.pkl"
    
    # If your app actually needs the API URL, uncomment the line below:
    api_url: str 

    # Pydantic V2 Configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"  # This fixes the crash by ignoring undeclared .env variables like api_url
    )

settings = Settings()
