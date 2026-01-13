import pyotp
from SmartApi.smartConnect import SmartConnect
from django.conf import settings
import logging
from .utils.redis_client import RedisClient
import threading
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


class AngelOneService:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        """Initialize service with configuration"""
        if not hasattr(self, 'initialized'):
            self.API_KEY = settings.ANGEL_ONE_API_KEY
            self.CLIENT_CODE = settings.ANGEL_ONE_CLIENT_CODE
            self.PASSWORD = settings.ANGEL_ONE_PASSWORD
            self.TOTP_SECRET = settings.ANGEL_ONE_TOTP_SECRET
            self.jwt_token = None
            self.feed_token = None
            self.refresh_token =None
            self.smartApi = None
            self.last_login = None
            self.initialized = True
            self.token_refresh_interval = timedelta(hours=8)  # Refresh tokens every 8 hours
            self._ensure_initialized()

    @classmethod
    def get_instance(cls):
        """Get or create singleton instance with thread safety"""
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = cls()
        return cls._instance

    def _ensure_initialized(self):
        """Ensure the service is properly initialized"""
        if not self.smartApi:
            try:
                self.smartApi = SmartConnect(api_key=self.API_KEY)
                self.login()
            except Exception as e:
                logger.error(f"Failed to initialize SmartApi: {e}")
                raise

    def login(self):
        """Perform login and token initialization"""
        try:
            # Generate TOTP
            totp = pyotp.TOTP(self.TOTP_SECRET)
            totp_code = totp.now()
            
            # Generate session with TOTP
            data = self.smartApi.generateSession(self.CLIENT_CODE, self.PASSWORD, totp_code)
            
            if data['status']:
                self.jwt_token = data['data']['jwtToken']
                self.refresh_token = data['data']['refreshToken']
                self.feed_token = self.smartApi.getfeedToken()
                self.last_login = datetime.now()
                logger.info("Successfully logged in to Angel One")
                return True
            else:
                logger.error(f"Login failed: {data.get('message', 'Unknown error')}")
                return False
        except Exception as e:
            logger.error(f"Login error: {e}")
            raise

    def ensure_login(self):
        """Ensure valid login session"""
        if not self.jwt_token or not self.feed_token:
            return self.login()
        
        if self.last_login and datetime.now() - self.last_login > self.token_refresh_interval:
            logger.info("Token refresh needed")
            return self.login()
        
        return True

    def _validate_tokens(self):
        """Validate current tokens"""
        if not self.jwt_token or not self.feed_token:
            return False
        
        if not self.last_login or datetime.now() - self.last_login > self.token_refresh_interval:
            return False
        
        return True

    def place_order(self, order_type, quantity, tradingsymbol, symboltoken, price=0):
        """
        Places an order (LIMIT / MARKET / SL).
        """
        if not self.smartApi:
            logger.warning("SmartAPI not initialized. Trying login again...")
            self.login()

        order_params = {
            "variety": "NORMAL",             # OR AMO, STOPLOSS_LIMIT, etc.
            "tradingsymbol": tradingsymbol,  # Example: 'KOTAKBANK-EQ'
            "symboltoken": symboltoken,      # Example: '1922'
            "transactiontype": order_type,   # 'BUY' or 'SELL'
            "exchange": 'NSE',            # 'NSE' or 'BSE'
            "ordertype": "LIMIT",            # OR MARKET, SL, etc.
            "producttype": "INTRADAY",       # OR DELIVERY
            "duration": "DAY",               # Validity
            "price": price,                  # Price for LIMIT orders
            "quantity": quantity
        }

        try:
            logger.info(f"📤 Placing order: {order_params}")
            order_response = self.smartApi.placeOrder(order_params)
            logger.info(f"✅ Order response: {order_response}")
            return order_response

        except Exception as e:
            logger.error(f"❌ Order placement failed: {e}")
            return {'error': str(e)}

    def get_holdings(self):
        """
        Returns user's current holdings.
        """
        if not self.smartApi:
            self.login()

        try:
            holdings = self.smartApi.holding()
            logger.info("✅ Holdings fetched successfully.")
            return holdings
        except Exception as e:
            logger.error(f"❌ Failed to fetch holdings: {e}")
            return {'error': str(e)}

    def get_profile(self):
        """
        Returns user profile.
        """
        if not self.smartApi:
            self.login()

        try:
            profile = self.smartApi.getProfile(self.jwt_token)
            logger.info("✅ Profile fetched successfully.")
            return profile
        except Exception as e:
            logger.error(f"❌ Failed to fetch profile: {e}")
            return {'error': str(e)}

    def logout(self):
        """
        Logs out of SmartAPI.
        """
        if not self.smartApi:
            return {'error': 'No active session'}

        try:
            response = self.smartApi.terminateSession(self.CLIENT_CODE)
            logger.info("✅ Logout successful.")
            return response
        except Exception as e:
            logger.error(f"❌ Logout failed: {e}")
            return {'error': str(e)} 
   