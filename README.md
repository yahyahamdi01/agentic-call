# Test technique
---


## PRÉREQUIS

Pour faire tourner ce projet, vous aurez besoin de :

* **Python** : Version 3.10 ou plus récente.
* **LiveKit Cloud** : Un compte (URL du projet, API Key et API Secret).
* **OpenAI** : Une clé API 

---

## INSTALLATION ET CONFIGURATION

### Étape 1 : Cloner le projet et créer un environnement virtuel
1.  Tapez `python -m venv venv` dans votre terminal.
2.  Pour activer l'environnement :
    * **macOS ou Linux** : `source venv/bin/activate`
    * **Windows** : `venv\Scripts\activate`
3.  Installez les bibliothèques avec : `pip install -r requirements.txt`

### Étape 2 : Configurer les variables d'environnement
Créez un fichier nommé `.env` à la racine du projet et ajoutez vos accès comme ceci :

```env
LIVEKIT_URL=votre_url_livekit
LIVEKIT_API_KEY=votre_cle_api
LIVEKIT_API_SECRET=votre_secret_api
OPENAI_API_KEY=votre_cle_openai
```
## LANCEMENT DU PROJET (HOW TO RUN)

Le projet nécessite deux terminaux ouverts simultanément :

### Terminal 1 : L'API Métier (Flask)
Tapez la commande :
`python api.py`

*L'API va créer automatiquement le fichier de base de données `appointments.db` et écoutera sur le port 5000.*

### Terminal 2 : L'Agent IA (LiveKit)
Tapez la commande :
`python agent.py dev`

*L'agent se connectera à votre instance LiveKit Cloud et attendra qu'un utilisateur rejoigne la session.*

---

## PROTOCOLE DE TEST 

1. **Connexion** : Rendez-vous sur le site [agents-playground.livekit.io](https://agents-playground.livekit.io).
2. **Configuration** : Dans les paramètres du Playground, entrez vos identifiants LiveKit (**Host**, **API Key**, **Secret**).
3. **Lancement** : Cliquez sur le bouton **"Connect"**.
4. **Interaction** : L'agent vous parlera immédiatement : *"Bonjour, bienvenue chez Bee2link. À quelle date souhaitez-vous prendre rendez-vous ?"*
5. **Action** : Dites une date à haute voix, par exemple : *"Le 12 avril"*.

### Résultat attendu :
* L'agent confirme vocalement et déclenche la fonction interne de sauvegarde.
* Dans le terminal de l'API Flask, vous verrez le message : `Appointment saved for: 12 avril`.
* L'appel se coupera tout seul après 5 secondes.
* Vous pourrez voir la nouvelle ligne enregistrée dans le fichier `appointments.db`.