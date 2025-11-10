"""
Dependency injection container for managing services.
"""

from typing import TypeVar, Type, Dict, Any, Callable
import logging

T = TypeVar('T')
logger = logging.getLogger(__name__)


class ServiceContainer:
    """Simple dependency injection container."""
    
    def __init__(self):
        self._services: Dict[Type, Any] = {}
        self._singletons: Dict[Type, Any] = {}
        self._factories: Dict[Type, Callable] = {}
        logger.info("ServiceContainer initialized")
    
    def register_singleton(self, interface: Type[T], implementation: Type[T]) -> 'ServiceContainer':
        """Register a singleton service."""
        self._services[interface] = (implementation, True)
        logger.debug(f"Registered singleton: {interface.__name__} -> {implementation.__name__}")
        return self
    
    def register_transient(self, interface: Type[T], implementation: Type[T]) -> 'ServiceContainer':
        """Register a transient service (new instance each time)."""
        self._services[interface] = (implementation, False)
        logger.debug(f"Registered transient: {interface.__name__} -> {implementation.__name__}")
        return self
    
    def register_factory(self, interface: Type[T], factory: Callable[[], T]) -> 'ServiceContainer':
        """Register a factory function for a service."""
        self._factories[interface] = factory
        logger.debug(f"Registered factory: {interface.__name__}")
        return self
    
    def register_instance(self, interface: Type[T], instance: T) -> 'ServiceContainer':
        """Register an existing instance as a singleton."""
        self._singletons[interface] = instance
        logger.debug(f"Registered instance: {interface.__name__}")
        return self
    
    def get(self, interface: Type[T]) -> T:
        """Get service instance."""
        # Check if we have a singleton instance
        if interface in self._singletons:
            return self._singletons[interface]
        
        # Check if we have a factory
        if interface in self._factories:
            instance = self._factories[interface]()
            logger.debug(f"Created instance from factory: {interface.__name__}")
            return instance
        
        # Check if we have a registered service
        if interface in self._services:
            implementation, is_singleton = self._services[interface]
            
            # Try to resolve dependencies automatically
            try:
                instance = self._create_instance(implementation)
                logger.debug(f"Created instance: {interface.__name__}")
                
                if is_singleton:
                    self._singletons[interface] = instance
                
                return instance
            except Exception as e:
                logger.error(f"Error creating instance for {interface.__name__}: {e}")
                raise
        
        raise ValueError(f"Service {interface.__name__} not registered")
    
    def _create_instance(self, implementation: Type[T]) -> T:
        """Create instance with dependency injection."""
        try:
            # Try to create without parameters first (for services without dependencies)
            return implementation()
        except TypeError as e:
            # If that fails, try to inject dependencies
            import inspect
            
            sig = inspect.signature(implementation.__init__)
            params = {}
            
            for param_name, param in sig.parameters.items():
                if param_name == 'self':
                    continue
                
                if param.annotation != param.empty:
                    # Try to resolve the dependency
                    try:
                        params[param_name] = self.get(param.annotation)
                    except ValueError:
                        if param.default == param.empty:
                            raise ValueError(f"Cannot resolve dependency {param.annotation} for {implementation.__name__}")
            
            return implementation(**params)
    
    def clear(self) -> None:
        """Clear all registrations."""
        self._services.clear()
        self._singletons.clear()
        self._factories.clear()
        logger.info("ServiceContainer cleared")
    
    def is_registered(self, interface: Type) -> bool:
        """Check if a service is registered."""
        return (interface in self._services or 
                interface in self._factories or 
                interface in self._singletons)