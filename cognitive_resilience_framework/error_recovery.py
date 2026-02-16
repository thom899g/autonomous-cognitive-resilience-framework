from typing import Dict, Optional
import logging

class RecoveryStrategy:
    """
    Base class for different recovery strategies.
    
    Each strategy represents a specific approach to recover from errors.
    """
    
    def __init__(self, name: str) -> None:
        self.name = name
        self.logger = logging.getLogger(f"Recovery.Strategy.{name}")
        
    @abstractmethod
    def apply_recovery(self, agent):
        pass
    
    @abstractmethod
    def is_applicable(self, error_state: Dict) -> bool:
        pass

class ResetParametersStrategy(RecoveryStrategy):
    """
    Recovery strategy that resets agent parameters to default values.
    Useful for recoveries where parameter corruption causes failures.
    """
    
    def apply_recovery(self, agent) -> None:
        try:
            # Reset all configurable parameters
            agent.configuration = get_default_parameters()
            self.logger.info("Parameters successfully reset to defaults")
            
        except Exception as e:
            self.logger.error(f"Failed to reset parameters: {str(e)}")
            raise RecoveryError("Parameter reset failed")

    def is_applicable(self, error_state: Dict) -> bool:
        # Check if the error is related to parameter corruption
        return "parameter_error" in error_state.get("error_types", [])

class ReinitializeComponentStrategy(RecoveryStrategy):
    """
    Recreates a specific component within the agent.
    Useful when component-specific failures occur.
    """
    
    def __init__(self, name: str, component_name: str) -> None:
        super().__init__(name)
        self.component_name = component_name
        
    def apply_recovery(self, agent) -> None:
        try:
            # Replace the failed component
            new_component = create_new_component()
            setattr(agent, self.component_name, new_component)
            self.logger.info(f"{self.component_name} successfully reinitialized")
            
        except Exception as e:
            self.logger.error(f"Failed to reinitialize {self.component_name}: {str(e)}")
            raise RecoveryError(f"{self.component_name} reinitialization failed")

    def is_applicable(self, error_state: Dict) -> bool:
        # Check if the error is related to component failure
        return "component_failure" in error_state.get("error_types", [])