from typing import Dict, Optional
import logging

class HealthMonitor:
    """
    Monitors the health of cognitive agents and triggers recovery actions.
    
    Implements a publish-subscribe pattern for error detection and recovery.
    """
    
    def __init__(self) -> None:
        self.logger = logging.getLogger("HealthMonitor")
        self.publishers = []
        
    def register_publisher(self, publisher):
        """
        Registers an agent to monitor its health.
        """
        self.publishers.append(publisher)
        self.logger.debug(f"Registered new publisher: {publisher.name}")
        
    def publish_error(self, error_data: Dict) -> None:
        """
        Notifies subscribers about detected errors.
        """
        for subscriber in self.publishers:
            if hasattr(subscriber, 'on_error'):
                try:
                    subscriber.on_error(error_data)
                    self.logger.debug(f"Successfully notified {subscriber.name} of error")
                    
                except Exception as e:
                    self.logger.error(f"Failed to notify {subscriber.name}: {str(e)}")

class CognitiveModuleErrorPublisher:
    """
    Publishes errors detected by cognitive modules.
    
    Implements the publisher part of the observer pattern.
    """
    
    def __init__(self, name: str) -> None:
        self.name = name
        self.health_monitor = HealthMonitor()
        
    def publish_error(self, error_data: Dict) -> None:
        """
        Publishes an error event to all subscribers.
        """
        self.health_monitor.publish_error(error_data)
    
    def on_error(self, error_data: Dict) -> None:
        """
        Callback for handling received errors.
        """
        pass  # To be implemented by specific modules