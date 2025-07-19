// src/hooks/useDynamicComponents.js - Dynamic Component Loading

import { useState, useEffect, useCallback } from 'react';
import { aetherAPI } from '../services/api';

// Cache for loaded components
const componentCache = new Map();

// Error boundary wrapper for dynamic components
const DynamicComponentWrapper = ({ Component, ...props }) => {
  try {
    return <Component {...props} />;
  } catch (error) {
    console.error('Error rendering dynamic component:', error);
    return (
      <div className="bg-red-900 bg-opacity-20 border border-red-500 rounded-lg p-4 text-red-400">
        <h3 className="font-bold">⚠️ Component Error</h3>
        <p className="text-sm mt-2">Failed to render dynamic component</p>
        <code className="text-xs mt-2 block">{error.message}</code>
      </div>
    );
  }
};

// Hook for loading dynamic components
export const useDynamicComponents = () => {
  const [rooms, setRooms] = useState([]);
  const [loadedComponents, setLoadedComponents] = useState(new Map());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Load component dynamically
  const loadComponent = useCallback(async (componentName, componentPath) => {
    try {
      // Check cache first
      if (componentCache.has(componentName)) {
        return componentCache.get(componentName);
      }

      // Try to import the component
      const moduleUrl = `/src/components/${componentName}.jsx`;
      
      // Use dynamic import with timestamp to avoid caching issues
      const timestamp = Date.now();
      const module = await import(`${moduleUrl}?t=${timestamp}`);
      
      const Component = module.default || module[componentName];
      
      if (!Component) {
        throw new Error(`Component ${componentName} not found in module`);
      }

      // Wrap component with error boundary
      const WrappedComponent = (props) => (
        <DynamicComponentWrapper Component={Component} {...props} />
      );

      // Cache the component
      componentCache.set(componentName, WrappedComponent);
      
      return WrappedComponent;
      
    } catch (error) {
      console.error(`Error loading component ${componentName}:`, error);
      
      // Return fallback component
      return ({ error: componentError }) => (
        <div className="bg-yellow-900 bg-opacity-20 border border-yellow-500 rounded-lg p-4 text-yellow-400">
          <h3 className="font-bold">🔄 Loading Component...</h3>
          <p className="text-sm mt-2">Component "{componentName}" not yet available</p>
          {componentError && (
            <code className="text-xs mt-2 block opacity-70">{componentError}</code>
          )}
        </div>
      );
    }
  }, []);

  // Fetch and load all available rooms
  const refreshComponents = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const roomsData = await aetherAPI.getRooms();
      
      if (roomsData.error) {
        setError(roomsData.error);
        return;
      }

      const availableRooms = roomsData.rooms || [];
      setRooms(availableRooms);

      // Load all components
      const newLoadedComponents = new Map();
      
      for (const room of availableRooms) {
        try {
          const component = await loadComponent(room.name, room.path);
          newLoadedComponents.set(room.name, {
            component,
            metadata: room,
            loadedAt: Date.now()
          });
        } catch (error) {
          console.error(`Failed to load room component ${room.name}:`, error);
        }
      }

      setLoadedComponents(newLoadedComponents);
      
    } catch (error) {
      console.error('Error refreshing components:', error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }, [loadComponent]);

  // Auto-refresh every 5 seconds
  useEffect(() => {
    refreshComponents();
    
    const interval = setInterval(refreshComponents, 5000);
    
    return () => clearInterval(interval);
  }, [refreshComponents]);

  // Get component by name
  const getComponent = useCallback((componentName) => {
    return loadedComponents.get(componentName);
  }, [loadedComponents]);

  // Get all loaded components
  const getAllComponents = useCallback(() => {
    return Array.from(loadedComponents.values());
  }, [loadedComponents]);

  return {
    rooms,
    loadedComponents: getAllComponents(),
    getComponent,
    refreshComponents,
    loading,
    error
  };
};

// Hook for loading individual component
export const useComponent = (componentName) => {
  const [component, setComponent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!componentName) return;

    const loadSingleComponent = async () => {
      try {
        setLoading(true);
        setError(null);

        // Check if component exists in rooms list first
        const roomsData = await aetherAPI.getRooms();
        const roomExists = roomsData.rooms?.find(room => room.name === componentName);

        if (!roomExists) {
          setError(`Component ${componentName} not found in available rooms`);
          return;
        }

        // Load the component
        const moduleUrl = `/src/components/${componentName}.jsx`;
        const timestamp = Date.now();
        const module = await import(`${moduleUrl}?t=${timestamp}`);
        
        const Component = module.default || module[componentName];
        
        if (!Component) {
          throw new Error(`Component ${componentName} not exported`);
        }

        setComponent(() => Component);
        
      } catch (error) {
        console.error(`Error loading component ${componentName}:`, error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    loadSingleComponent();
  }, [componentName]);

  return { component, loading, error };
};

export default useDynamicComponents; 