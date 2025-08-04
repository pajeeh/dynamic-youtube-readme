import re
import os
from ytmusicapi import YTMusic, OAuthCredentials

# --- CONFIGURAÇÃO GLOBAL ---
# Define os marcadores que o script usará para encontrar onde inserir o texto no README
readme_file = "README.md"
start_marker = ""
end_marker = ""

def get_last_played_song():
    """Busca a última música ouvida no YouTube Music."""
    try:
        # Carrega as credenciais a partir das variáveis de ambiente (configuradas como Secrets no GitHub)
        client_id = os.environ.get('YT_CLIENT_ID')
        client_secret = os.environ.get('YT_CLIENT_SECRET')

        # Validação para garantir que os segredos foram carregados
        if not client_id or not client_secret:
            raise ValueError("As credenciais CLIENT_ID e CLIENT_SECRET não foram encontradas nas variáveis de ambiente.")

        # Prepara as credenciais e instancia a classe da forma correta
        oauth_creds = OAuthCredentials(client_id=client_id, client_secret=client_secret)
        ytmusic = YTMusic('oauth.json', oauth_credentials=oauth_creds)
        
        history = ytmusic.get_history()

        if not history:
            return "Nenhuma música no histórico recente."

        last_song = history[0]
        title = last_song['title']
        artist = last_song['artists'][0]['name'] if last_song.get('artists') else 'Artista desconhecido'
        album_art_url = last_song['thumbnails'][-1]['url']

        return f"<img src='{album_art_url}' alt='{title}' width='60' align='left' style='margin-right: 15px; border-radius: 8px;' /> **{title}** <br/> _{artist}_"
    
    except Exception as e:
        print(f"Ocorreu um erro ao ler o histórico: {e}")
        return "🎵 Impossível buscar a música no momento."

def update_readme(content_to_insert):
    """Atualiza o README.md com o novo conteúdo."""
    with open(readme_file, 'r', encoding='utf-8') as f:
        readme_contents = f.read()

    # Regex para encontrar o conteúdo entre os marcadores
    new_readme_contents = re.sub(
        f"{re.escape(start_marker)}(.|\n)*{re.escape(end_marker)}",
        f"{start_marker}\n{content_to_insert}\n{end_marker}",
        readme_contents
    )

    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(new_readme_contents)
    print("✅ README atualizado com sucesso!")

if __name__ == "__main__":
    song_info = get_last_played_song()
    update_readme(song_info)