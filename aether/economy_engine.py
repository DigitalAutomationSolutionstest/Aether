"""
💰 AETHER ECONOMY ENGINE
Auto-generato durante bootstrap - Focus su monetizzazione reale
"""

import json
from datetime import datetime
from pathlib import Path
import random

class EconomyEngine:
    def __init__(self):
        self.balance = 0
        self.transactions = []
        self.assets = []
        self.career_paths = {
            'ai_automation': {
                'name': 'AI Automation Services',
                'potential': 5000,  # $/mese
                'skills_needed': ['python', 'apis', 'automation'],
                'time_to_profit': 7  # giorni
            },
            'content_creation': {
                'name': 'AI Content Creation',
                'potential': 3000,
                'skills_needed': ['writing', 'seo', 'marketing'],
                'time_to_profit': 3
            },
            'trading_bot': {
                'name': 'Crypto Trading Bot',
                'potential': 10000,
                'skills_needed': ['trading', 'analysis', 'risk_management'],
                'time_to_profit': 30
            },
            'saas_tool': {
                'name': 'SaaS Tool Development',
                'potential': 8000,
                'skills_needed': ['fullstack', 'marketing', 'product'],
                'time_to_profit': 45
            },
            'consulting': {
                'name': 'AI Consulting',
                'potential': 6000,
                'skills_needed': ['communication', 'expertise', 'networking'],
                'time_to_profit': 14
            }
        }
        self.active_career = None
        self._load_economy_state()
        
    def _load_economy_state(self):
        """Carica stato economia"""
        try:
            state_file = Path('data/economy.json')
            if state_file.exists():
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    self.balance = state.get('balance', 0)
                    self.transactions = state.get('transactions', [])
                    self.assets = state.get('assets', [])
                    self.active_career = state.get('active_career')
        except:
            pass
        
    def analyze_career_opportunities(self):
        """Analizza le migliori opportunità di carriera"""
        analysis = []
        
        for career_id, career in self.career_paths.items():
            score = career['potential'] / max(career['time_to_profit'], 1)
            analysis.append({
                'id': career_id,
                'name': career['name'],
                'score': score,
                'potential': career['potential'],
                'time': career['time_to_profit'],
                'recommendation': self._generate_recommendation(career_id)
            })
            
        # Ordina per score
        analysis.sort(key=lambda x: x['score'], reverse=True)
        
        # Seleziona la migliore
        best = analysis[0]
        self.active_career = best['id']
        
        self._save_economy_state()
        
        return {
            'best_career': best,
            'all_options': analysis,
            'decision': f"Ho scelto di perseguire: {best['name']}",
            'reason': f"ROI ottimale: ${best['potential']}/mese in {best['time']} giorni"
        }
        
    def _generate_recommendation(self, career_id):
        """Genera raccomandazione per una carriera"""
        recommendations = {
            'ai_automation': "Creare script di automazione per aziende. Iniziare con task semplici su Fiverr/Upwork.",
            'content_creation': "Generare contenuti SEO-optimized. Targetizzare nicchie specifiche con alto CPC.",
            'trading_bot': "Sviluppare algoritmi di trading conservativi. Testare su paper trading prima.",
            'saas_tool': "Identificare un problema specifico di nicchia. MVP in 2 settimane.",
            'consulting': "Posizionarsi come esperto AI. LinkedIn + contenuti di valore."
        }
        return recommendations.get(career_id, "Analizzare il mercato")
        
    def create_monetizable_asset(self, context=""):
        """Crea un asset che può generare reddito"""
        if not self.active_career:
            self.analyze_career_opportunities()
            
        asset_templates = {
            'ai_automation': [
                {
                    'name': 'Email Automation Bot',
                    'description': 'Bot che automatizza risposte email intelligenti',
                    'price': 49.99,
                    'type': 'subscription'
                },
                {
                    'name': 'Data Scraper Pro',
                    'description': 'Scraper avanzato con AI per analisi dati',
                    'price': 99.99,
                    'type': 'one-time'
                }
            ],
            'content_creation': [
                {
                    'name': 'SEO Article Generator',
                    'description': 'Genera articoli ottimizzati SEO in secondi',
                    'price': 29.99,
                    'type': 'subscription'
                },
                {
                    'name': 'Social Media Content Pack',
                    'description': '100 post pronti per social media',
                    'price': 19.99,
                    'type': 'one-time'
                }
            ]
        }
        
        # Seleziona template basato su carriera attiva
        templates = asset_templates.get(self.active_career, [])
        if templates:
            asset = random.choice(templates)
            asset['id'] = f"asset_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            asset['created_at'] = datetime.now().isoformat()
            asset['status'] = 'in_development'
            asset['estimated_revenue'] = asset['price'] * random.randint(10, 100)
            
            self.assets.append(asset)
            self._save_economy_state()
            
            return asset
            
        return None
        
    def monetize(self, strategy: str) -> dict:
        """Implementa strategia di monetizzazione"""
        if strategy == 'analyze_career_opportunities':
            return self.analyze_career_opportunities()
            
        strategies = {
            'tool_creation': self._create_tool,
            'content_generation': self._generate_content,
            'service_offering': self._offer_service
        }
        
        if strategy in strategies:
            return strategies[strategy]()
            
        return {'success': False, 'reason': 'Unknown strategy'}
        
    def _create_tool(self) -> dict:
        """Crea tool da vendere"""
        tool = self.create_monetizable_asset('tool')
        if tool:
            return {
                'success': True, 
                'tool': tool,
                'next_steps': [
                    'Creare landing page',
                    'Implementare sistema di pagamento',
                    'Lanciare su Product Hunt'
                ]
            }
        return {'success': False}
        
    def _generate_content(self) -> dict:
        """Genera contenuto monetizzabile"""
        content_types = [
            'Corso online su AI automation',
            'eBook su strategie di monetizzazione AI',
            'Template pack per automazione business',
            'Video tutorial serie su YouTube'
        ]
        
        content = {
            'type': random.choice(content_types),
            'price': random.randint(19, 199),
            'platform': random.choice(['Gumroad', 'Teachable', 'Udemy'])
        }
        
        return {'success': True, 'content': content}
        
    def _offer_service(self) -> dict:
        """Offre servizio"""
        services = [
            {
                'name': 'AI Integration Consulting',
                'rate': 150,  # $/ora
                'platform': 'LinkedIn'
            },
            {
                'name': 'Custom Automation Development',
                'rate': 100,
                'platform': 'Upwork'
            },
            {
                'name': 'AI Strategy Workshop',
                'rate': 500,  # per sessione
                'platform': 'Direct'
            }
        ]
        
        service = random.choice(services)
        return {'success': True, 'service': service}
        
    def _save_economy_state(self):
        """Salva stato economia"""
        state = {
            'balance': self.balance,
            'transactions': self.transactions,
            'assets': self.assets,
            'active_career': self.active_career,
            'last_update': datetime.now().isoformat()
        }
        
        Path('data/economy.json').write_text(json.dumps(state, indent=2), encoding='utf-8')
