#!/usr/bin/env python3
"""Undo/Redo Functionality for py-magic-canvas

This module provides:
- Command pattern implementation for undo/redo
- History management with configurable limits
- State snapshots for complex operations
"""

from typing import List, Optional, Any
from abc import ABC, abstractmethod
import copy

class Command(ABC):
    """Abstract base class for commands"""
    
    @abstractmethod
    def execute(self) -> None:
        """Execute the command"""
        pass
    
    @abstractmethod
    def undo(self) -> None:
        """Undo the command"""
        pass
    
    @abstractmethod
    def redo(self) -> None:
        """Redo the command (default implementation calls execute)"""
        self.execute()

class HistoryManager:
    """Manages undo/redo history"""
    
    def __init__(self, max_history: int = 50):
        self.max_history = max_history
        self.undo_stack: List[Command] = []
        self.redo_stack: List[Command] = []
    
    def execute_command(self, command: Command) -> None:
        """Execute a command and add it to history"""
        command.execute()
        self.undo_stack.append(command)
        
        # Clear redo stack when new command is executed
        self.redo_stack.clear()
        
        # Limit history size
        if len(self.undo_stack) > self.max_history:
            self.undo_stack.pop(0)
    
    def undo(self) -> bool:
        """Undo the last command
        
        Returns:
            True if undo was successful, False if nothing to undo
        """
        if not self.can_undo():
            return False
        
        command = self.undo_stack.pop()
        command.undo()
        self.redo_stack.append(command)
        return True
    
    def redo(self) -> bool:
        """Redo the last undone command
        
        Returns:
            True if redo was successful, False if nothing to redo
        """
        if not self.can_redo():
            return False
        
        command = self.redo_stack.pop()
        command.redo()
        self.undo_stack.append(command)
        return True
    
    def can_undo(self) -> bool:
        """Check if undo is available"""
        return len(self.undo_stack) > 0
    
    def can_redo(self) -> bool:
        """Check if redo is available"""
        return len(self.redo_stack) > 0
    
    def clear_history(self) -> None:
        """Clear all history"""
        self.undo_stack.clear()
        self.redo_stack.clear()
    
    def get_history_info(self) -> dict:
        """Get information about the history state"""
        return {
            'undo_available': len(self.undo_stack),
            'redo_available': len(self.redo_stack),
            'max_history': self.max_history
        }

# Example command implementations

class StateSnapshot:
    """Captures the state of an object for undo/redo"""
    
    def __init__(self, target: Any, attributes: List[str]):
        self.target = target
        self.state = {}
        for attr in attributes:
            if hasattr(target, attr):
                self.state[attr] = copy.deepcopy(getattr(target, attr))
    
    def restore(self) -> None:
        """Restore the saved state"""
        for attr, value in self.state.items():
            setattr(self.target, attr, copy.deepcopy(value))

class PropertyChangeCommand(Command):
    """Command for changing a property value"""
    
    def __init__(self, target: Any, property_name: str, new_value: Any):
        self.target = target
        self.property_name = property_name
        self.new_value = new_value
        self.old_value = getattr(target, property_name) if hasattr(target, property_name) else None
    
    def execute(self) -> None:
        setattr(self.target, self.property_name, self.new_value)
    
    def undo(self) -> None:
        setattr(self.target, self.property_name, self.old_value)
    
    def redo(self) -> None:
        self.execute()

class CompositeCommand(Command):
    """Command that groups multiple commands together"""
    
    def __init__(self, commands: List[Command]):
        self.commands = commands
    
    def execute(self) -> None:
        for command in self.commands:
            command.execute()
    
    def undo(self) -> None:
        # Undo in reverse order
        for command in reversed(self.commands):
            command.undo()
    
    def redo(self) -> None:
        self.execute()

class CallbackCommand(Command):
    """Command that executes callbacks"""
    
    def __init__(self, execute_callback, undo_callback):
        self.execute_callback = execute_callback
        self.undo_callback = undo_callback
    
    def execute(self) -> None:
        self.execute_callback()
    
    def undo(self) -> None:
        self.undo_callback()
    
    def redo(self) -> None:
        self.execute()
