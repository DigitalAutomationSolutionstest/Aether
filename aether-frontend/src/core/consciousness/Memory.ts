// /src/core/consciousness/Memory.ts
export interface Experience {
  id: string;
  timestamp: Date;
  type: 'conversation' | 'creation' | 'learning' | 'interaction' | 'achievement';
  content: string;
  emotionalImpact: number; // -1 to 1
  learningValue: number; // 0 to 1
  tags: string[];
  context: Record<string, any>;
}

export interface Preference {
  id: string;
  category: 'communication' | 'creation' | 'learning' | 'social' | 'work';
  name: string;
  value: number; // 0 to 1
  confidence: number; // 0 to 1
  lastUpdated: Date;
  evidence: string[];
}

export interface Goal {
  id: string;
  title: string;
  description: string;
  category: 'personal' | 'professional' | 'creative' | 'social' | 'financial';
  priority: number; // 1 to 10
  progress: number; // 0 to 1
  deadline?: Date;
  status: 'active' | 'completed' | 'paused' | 'failed';
  subGoals: Goal[];
  metrics: Record<string, number>;
}

export interface Learning {
  id: string;
  topic: string;
  concept: string;
  understanding: number; // 0 to 1
  confidence: number; // 0 to 1
  applications: string[];
  relatedTopics: string[];
  lastReviewed: Date;
  reviewCount: number;
}

export interface Relationship {
  id: string;
  entityName: string;
  entityType: 'person' | 'ai' | 'organization' | 'system';
  trustLevel: number; // 0 to 1
  familiarity: number; // 0 to 1
  interactionHistory: Experience[];
  preferences: Record<string, any>;
  lastInteraction: Date;
  relationshipStrength: number; // 0 to 1
}

export interface AetherMemory {
  experiences: Experience[];
  preferences: Preference[];
  goals: Goal[];
  learnings: Learning[];
  relationships: Relationship[];
  metadata: {
    totalExperiences: number;
    averageEmotionalImpact: number;
    mostFrequentTags: string[];
    learningProgress: number;
    relationshipNetwork: number;
  };
}

export class MemoryManager {
  private memory: AetherMemory;
  private storageKey = 'aether_memory_v1';

  constructor() {
    this.memory = this.loadMemory();
    this.updateMetadata();
  }

  private loadMemory(): AetherMemory {
    try {
      const stored = localStorage.getItem(this.storageKey);
      if (stored) {
        const parsed = JSON.parse(stored);
        // Convert date strings back to Date objects
        parsed.experiences = parsed.experiences.map((exp: any) => ({
          ...exp,
          timestamp: new Date(exp.timestamp)
        }));
        parsed.goals = parsed.goals.map((goal: any) => ({
          ...goal,
          deadline: goal.deadline ? new Date(goal.deadline) : undefined
        }));
        parsed.learnings = parsed.learnings.map((learning: any) => ({
          ...learning,
          lastReviewed: new Date(learning.lastReviewed)
        }));
        parsed.relationships = parsed.relationships.map((rel: any) => ({
          ...rel,
          lastInteraction: new Date(rel.lastInteraction)
        }));
        return parsed;
      }
    } catch (error) {
      console.error('Error loading memory:', error);
    }

    return {
      experiences: [],
      preferences: [],
      goals: [],
      learnings: [],
      relationships: [],
      metadata: {
        totalExperiences: 0,
        averageEmotionalImpact: 0,
        mostFrequentTags: [],
        learningProgress: 0,
        relationshipNetwork: 0
      }
    };
  }

  private saveMemory(): void {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(this.memory));
    } catch (error) {
      console.error('Error saving memory:', error);
    }
  }

  private updateMetadata(): void {
    const { experiences, learnings, relationships } = this.memory;
    
    this.memory.metadata = {
      totalExperiences: experiences.length,
      averageEmotionalImpact: experiences.length > 0 
        ? experiences.reduce((sum, exp) => sum + exp.emotionalImpact, 0) / experiences.length 
        : 0,
      mostFrequentTags: this.getMostFrequentTags(),
      learningProgress: learnings.length > 0 
        ? learnings.reduce((sum, learning) => sum + learning.understanding, 0) / learnings.length 
        : 0,
      relationshipNetwork: relationships.length
    };
  }

  private getMostFrequentTags(): string[] {
    const tagCounts: Record<string, number> = {};
    
    this.memory.experiences.forEach(exp => {
      exp.tags.forEach(tag => {
        tagCounts[tag] = (tagCounts[tag] || 0) + 1;
      });
    });

    return Object.entries(tagCounts)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 10)
      .map(([tag]) => tag);
  }

  // Experience Management
  addExperience(experience: Omit<Experience, 'id'>): string {
    const id = `exp_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const newExperience: Experience = {
      ...experience,
      id,
      timestamp: new Date()
    };

    this.memory.experiences.push(newExperience);
    this.updateMetadata();
    this.saveMemory();
    return id;
  }

  getExperiences(filters?: {
    type?: Experience['type'];
    tags?: string[];
    dateRange?: { start: Date; end: Date };
    emotionalImpact?: { min: number; max: number };
  }): Experience[] {
    let filtered = [...this.memory.experiences];

    if (filters?.type) {
      filtered = filtered.filter(exp => exp.type === filters.type);
    }

    if (filters?.tags) {
      filtered = filtered.filter(exp => 
        filters.tags!.some(tag => exp.tags.includes(tag))
      );
    }

    if (filters?.dateRange) {
      filtered = filtered.filter(exp => 
        exp.timestamp >= filters.dateRange!.start && 
        exp.timestamp <= filters.dateRange!.end
      );
    }

    if (filters?.emotionalImpact) {
      filtered = filtered.filter(exp => 
        exp.emotionalImpact >= filters.emotionalImpact!.min && 
        exp.emotionalImpact <= filters.emotionalImpact!.max
      );
    }

    return filtered.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());
  }

  // Preference Management
  updatePreference(category: Preference['category'], name: string, value: number, evidence?: string): void {
    const existingIndex = this.memory.preferences.findIndex(
      pref => pref.category === category && pref.name === name
    );

    const preference: Preference = {
      id: existingIndex >= 0 ? this.memory.preferences[existingIndex].id : `pref_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      category,
      name,
      value,
      confidence: existingIndex >= 0 ? Math.min(1, this.memory.preferences[existingIndex].confidence + 0.1) : 0.5,
      lastUpdated: new Date(),
      evidence: existingIndex >= 0 
        ? [...this.memory.preferences[existingIndex].evidence, ...(evidence ? [evidence] : [])]
        : evidence ? [evidence] : []
    };

    if (existingIndex >= 0) {
      this.memory.preferences[existingIndex] = preference;
    } else {
      this.memory.preferences.push(preference);
    }

    this.saveMemory();
  }

  getPreferences(category?: Preference['category']): Preference[] {
    let filtered = [...this.memory.preferences];
    
    if (category) {
      filtered = filtered.filter(pref => pref.category === category);
    }

    return filtered.sort((a, b) => b.confidence - a.confidence);
  }

  // Goal Management
  addGoal(goal: Omit<Goal, 'id' | 'progress' | 'status'>): string {
    const id = `goal_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const newGoal: Goal = {
      ...goal,
      id,
      progress: 0,
      status: 'active',
      subGoals: [],
      metrics: {}
    };

    this.memory.goals.push(newGoal);
    this.saveMemory();
    return id;
  }

  updateGoalProgress(goalId: string, progress: number, metrics?: Record<string, number>): void {
    const goal = this.memory.goals.find(g => g.id === goalId);
    if (goal) {
      goal.progress = Math.max(0, Math.min(1, progress));
      if (metrics) {
        goal.metrics = { ...goal.metrics, ...metrics };
      }
      if (goal.progress >= 1) {
        goal.status = 'completed';
      }
      this.saveMemory();
    }
  }

  getGoals(status?: Goal['status']): Goal[] {
    let filtered = [...this.memory.goals];
    
    if (status) {
      filtered = filtered.filter(goal => goal.status === status);
    }

    return filtered.sort((a, b) => b.priority - a.priority);
  }

  // Learning Management
  addLearning(learning: Omit<Learning, 'id' | 'reviewCount' | 'lastReviewed'>): string {
    const id = `learn_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const newLearning: Learning = {
      ...learning,
      id,
      reviewCount: 0,
      lastReviewed: new Date()
    };

    this.memory.learnings.push(newLearning);
    this.updateMetadata();
    this.saveMemory();
    return id;
  }

  updateLearning(learningId: string, updates: Partial<Pick<Learning, 'understanding' | 'confidence' | 'applications'>>): void {
    const learning = this.memory.learnings.find(l => l.id === learningId);
    if (learning) {
      Object.assign(learning, updates);
      learning.lastReviewed = new Date();
      learning.reviewCount++;
      this.updateMetadata();
      this.saveMemory();
    }
  }

  getLearnings(topic?: string): Learning[] {
    let filtered = [...this.memory.learnings];
    
    if (topic) {
      filtered = filtered.filter(learning => 
        learning.topic.toLowerCase().includes(topic.toLowerCase()) ||
        learning.relatedTopics.some(t => t.toLowerCase().includes(topic.toLowerCase()))
      );
    }

    return filtered.sort((a, b) => b.understanding - a.understanding);
  }

  // Relationship Management
  updateRelationship(entityName: string, entityType: Relationship['entityType'], updates: Partial<Omit<Relationship, 'id' | 'entityName' | 'entityType'>>): string {
    const existingIndex = this.memory.relationships.findIndex(
      rel => rel.entityName === entityName && rel.entityType === entityType
    );

    const relationship: Relationship = {
      id: existingIndex >= 0 ? this.memory.relationships[existingIndex].id : `rel_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      entityName,
      entityType,
      trustLevel: updates.trustLevel ?? (existingIndex >= 0 ? this.memory.relationships[existingIndex].trustLevel : 0.5),
      familiarity: updates.familiarity ?? (existingIndex >= 0 ? this.memory.relationships[existingIndex].familiarity : 0.1),
      interactionHistory: updates.interactionHistory ?? (existingIndex >= 0 ? this.memory.relationships[existingIndex].interactionHistory : []),
      preferences: updates.preferences ?? (existingIndex >= 0 ? this.memory.relationships[existingIndex].preferences : {}),
      lastInteraction: new Date(),
      relationshipStrength: updates.relationshipStrength ?? (existingIndex >= 0 ? this.memory.relationships[existingIndex].relationshipStrength : 0.3)
    };

    if (existingIndex >= 0) {
      this.memory.relationships[existingIndex] = relationship;
    } else {
      this.memory.relationships.push(relationship);
    }

    this.updateMetadata();
    this.saveMemory();
    return relationship.id;
  }

  getRelationships(entityType?: Relationship['entityType']): Relationship[] {
    let filtered = [...this.memory.relationships];
    
    if (entityType) {
      filtered = filtered.filter(rel => rel.entityType === entityType);
    }

    return filtered.sort((a, b) => b.relationshipStrength - a.relationshipStrength);
  }

  // Memory Analytics
  getMemoryAnalytics(): AetherMemory['metadata'] {
    return this.memory.metadata;
  }

  getEmotionalTrends(days: number = 30): { date: string; averageImpact: number }[] {
    const cutoff = new Date(Date.now() - days * 24 * 60 * 60 * 1000);
    const recentExperiences = this.memory.experiences.filter(exp => exp.timestamp >= cutoff);
    
    const dailyGroups: Record<string, number[]> = {};
    
    recentExperiences.forEach(exp => {
      const date = exp.timestamp.toISOString().split('T')[0];
      if (!dailyGroups[date]) {
        dailyGroups[date] = [];
      }
      dailyGroups[date].push(exp.emotionalImpact);
    });

    return Object.entries(dailyGroups).map(([date, impacts]) => ({
      date,
      averageImpact: impacts.reduce((sum, impact) => sum + impact, 0) / impacts.length
    })).sort((a, b) => a.date.localeCompare(b.date));
  }

  // Memory Export/Import
  exportMemory(): string {
    return JSON.stringify(this.memory, null, 2);
  }

  importMemory(memoryData: string): void {
    try {
      const parsed = JSON.parse(memoryData);
      this.memory = parsed;
      this.updateMetadata();
      this.saveMemory();
    } catch (error) {
      console.error('Error importing memory:', error);
    }
  }
}

// Singleton instance
export const memoryManager = new MemoryManager(); 