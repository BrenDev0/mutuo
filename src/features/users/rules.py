from abc import ABC, abstractmethod

class EmailAvailability(ABC):
    """
    Check if email is availible before user registration
    """
    @abstractmethod
    async def validate(
        self, 
        email: str
    ) -> bool:
        """
        check if users email is avalailible

        Args:
            email: The email the client gives
        
        returns: 
            True if email is not found in db, False if found
        """
        raise NotImplementedError