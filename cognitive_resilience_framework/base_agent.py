from abc import ABC, abstractmethod
import logging
from typing import Dict, Optional

class CognitiveAgent(ABC):
    """
    Abstract Base Class for all Cognitive Agents in the Evolution Ecosystem.
    
    This class enforces common functionality and error handling across agents.
    Subclasses must implement specific domain logic while adhering to this structure.
    """

    def __init__(self, name: str, configuration: Dict) -> None:
        self.name = name
        self.configuration = configuration
        self.logger = logging.getLogger(f"Agent.{name}")
        
        # Initialize error tracking
        self.error_state = ErrorState()
        self.active_recovery_strategy: Optional[RecoveryStrategy] = None
        
    @abstractmethod
    def process_input(self, input_data):
        pass
    
    def monitor_health(self) -> bool:
        """
        Periodically checks the health of the agent.
        
        Returns True if healthy, False otherwise.
        """
        try:
            # Simulate health check logic
            self.logger.debug("Running health check...")
            
            # If any component reports failure
            for component in self.components:
                if not component.is_healthy():
                    self.logger.warning(f"Component {component.name} reported failure.")
                    return False
            
            return True
            
        except Exception as e:
            self.log_error(e, "Health monitoring failed")
            return False
    
    def apply_recovery_strategy(self, strategy: RecoveryStrategy) -> None:
        """
        Applies a recovery strategy in case of detected errors.
        """
        if self.active_recovery_strategy is not None:
            self.logger.info("Canceling current recovery operation.")
            self.active_recovery_strategy.cancel()
            
        self.active_recovery_strategy = strategy
        self.logger.info(f"Applying recovery strategy: {strategy.name}")
        
        try:
            # Execute the recovery steps
            strategy.apply_recovery(self)
            self.log_operation_success(strategy.name, "Recovery applied successfully")
            
        except Exception as e:
            self.log_error(e, f"Failure during {strategy.name} application")
            raise RecoveryStrategyError(f"{strategy.name} failed to apply")

    def log_operation_success(self, operation: str, message: str) -> None:
        """
        Logs successful completion of an operation.
        """
        self.logger.info(f"{operation}: {message}")
    
    def log_error(self, error: Exception, context: str) -> None:
        """
        Records errors with detailed context for debugging.
        """
        self.error_state.log_error(error, context)
        self.logger.error(f"Error in {context}: {str(error)}")