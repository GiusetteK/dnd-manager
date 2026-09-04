"""
Web interface for D&D Manager using Flask
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
from dnd_manager.characters import Character, CharacterGenerator
from dnd_manager.campaigns import Campaign
from dnd_manager.database import Storage

app = Flask(__name__, template_folder='templates', static_folder='static')
storage = Storage()


# Main Routes
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


# Character Routes
@app.route('/characters')
def characters():
    """List all characters"""
    char_list = storage.list_characters()
    characters_data = []
    
    for char_name in char_list:
        data = storage.load_character(char_name)
        if data:
            characters_data.append({
                'name': data['name'],
                'class': data['class'],
                'race': data['race'],
                'level': data['level'],
                'hp': f"{data['hit_points']}/{data['max_hit_points']}"
            })
    
    return render_template('characters.html', characters=characters_data)


@app.route('/character/new', methods=['GET', 'POST'])
def new_character():
    """Create a new character"""
    if request.method == 'POST':
        data = request.get_json()
        
        character = Character(
            name=data['name'],
            char_class=data['class'],
            race=data['race'],
            level=int(data.get('level', 1)),
            strength=int(data.get('strength', 10)),
            dexterity=int(data.get('dexterity', 10)),
            constitution=int(data.get('constitution', 10)),
            intelligence=int(data.get('intelligence', 10)),
            wisdom=int(data.get('wisdom', 10)),
            charisma=int(data.get('charisma', 10))
        )
        
        character_data = character.get_stats()
        
        if storage.save_character(data['name'], character_data):
            return jsonify({'success': True, 'message': f"Character {data['name']} created!"})
        else:
            return jsonify({'success': False, 'message': 'Error creating character'}), 400
    
    return render_template('character_form.html', 
                         classes=Character.CLASSES,
                         races=Character.RACES)


@app.route('/character/<name>')
def view_character(name):
    """View character details"""
    data = storage.load_character(name)
    if not data:
        return redirect(url_for('characters'))
    
    return render_template('character_view.html', character=data)


@app.route('/character/generate', methods=['POST'])
def generate_character():
    """Generate a random character"""
    data = request.get_json()
    character = CharacterGenerator.generate(name=data.get('name'))
    character_data = character.get_stats()
    
    if storage.save_character(character_data['name'], character_data):
        return jsonify({'success': True, 'character': character_data})
    else:
        return jsonify({'success': False}), 400


# Campaign Routes
@app.route('/campaigns')
def campaigns():
    """List all campaigns"""
    campaign_list = storage.list_campaigns()
    campaigns_data = []
    
    for campaign_name in campaign_list:
        data = storage.load_campaign(campaign_name)
        if data:
            campaigns_data.append({
                'name': data['name'],
                'game_master': data['game_master'],
                'setting': data['setting'],
                'party_level': data['party_level'],
                'status': data['status'],
                'sessions': len(data['sessions'])
            })
    
    return render_template('campaigns.html', campaigns=campaigns_data)


@app.route('/campaign/new', methods=['GET', 'POST'])
def new_campaign():
    """Create a new campaign"""
    if request.method == 'POST':
        data = request.get_json()
        
        campaign = Campaign(
            name=data['name'],
            game_master=data['gm'],
            setting=data.get('setting', 'Forgotten Realms'),
            description=data.get('description', '')
        )
        
        campaign_data = {
            "name": campaign.name,
            "game_master": campaign.game_master,
            "setting": campaign.setting,
            "description": campaign.description,
            "status": campaign.status,
            "party_level": campaign.party_level,
            "characters": campaign.characters,
            "npcs": campaign.npcs,
            "locations": campaign.locations,
            "quests": campaign.quests,
            "sessions": campaign.sessions,
            "created_at": campaign.created_at.isoformat()
        }
        
        if storage.save_campaign(data['name'], campaign_data):
            return jsonify({'success': True, 'message': f"Campaign {data['name']} created!"})
        else:
            return jsonify({'success': False}), 400
    
    return render_template('campaign_form.html')


@app.route('/campaign/<name>')
def view_campaign(name):
    """View campaign details"""
    data = storage.load_campaign(name)
    if not data:
        return redirect(url_for('campaigns'))
    
    return render_template('campaign_view.html', campaign=data)


# API Routes
@app.route('/api/stats')
def get_stats():
    """Get app statistics"""
    return jsonify({
        'characters': len(storage.list_characters()),
        'campaigns': len(storage.list_campaigns())
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
