from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

NOTION_DATABASE_ID = "1f630ca776c280b48febfbe7bdf9aba1"
NOTION_API_KEY = "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"
NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_VERSION = "2022-06-28"

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION
}

def create_notion_page(data):
    payload = {
        "parent": { "database_id": NOTION_DATABASE_ID },
        "properties": {
            "Nome do Cliente": {
                "title": [{ "text": { "content": data.get("nome_cliente", "") } }]
            },
            "Status": {
                "select": { "name": data.get("status", "Aguardando Pesquisa") }
            },
            "Tipo de Viagem": {
                "select": { "name": data.get("tipo_viagem", "Passagem Aérea") }
            },
            "Origem → Destino": {
                "rich_text": [{ "text": { "content": data.get("origem_destino", "") } }]
            },
            "Data de Ida": {
                "date": { "start": data.get("data_ida") }
                if data.get("data_ida") and "-" in data.get("data_ida") else None
            },
            "Data de Volta (se houver)": {
                "date": { "start": data.get("data_volta") }
                if data.get("data_volta") and "-" in data.get("data_volta") else None
            },
            "Qtd. de Passageiros": {
                "rich_text": [{ "text": { "content": data.get("qtd_passageiros", "") } }]
            },
            "Preferências": {
                "rich_text": [{ "text": { "content": data.get("preferencias", "") } }]
            },
            "Perfil de Viagem": {
                "select": { "name": data.get("perfil_viagem", "Econômico") }
            },
            "Vindo de post do Instagram?": {
                "checkbox": data.get("veio_instagram", False)
            },
            "Print enviado?": {
                "files": [{
                    "name": "print.jpg",
                    "external": { "url": data.get("print_enviado_url", "") }
                }] if data.get("print_enviado_url") else []
            },
            "Orçamento Validado (R$)": {
                "rich_text": [{ "text": { "content": data.get("orcamento_validado", "") } }]
            },
            "Observações Adicionais": {
                "rich_text": [{ "text": { "content": data.get("observacoes", "") } }]
            }
        }
    }

    # Remove campos None
    payload["properties"] = {k: v for k, v in payload["properties"].items() if v is not None}

    try:
        response = requests.post(NOTION_API_URL, headers=HEADERS, json=payload)
        print("NOTION RESPONSE:", response.status_code, response.text)
        return response.status_code, response.json()
    except Exception as e:
        print("ERRO AO ENVIAR PARA O NOTION:", e)
        return 500, {"error": str(e)}


@app.route("/notion/enviar-solicitacao", methods=["POST"])
def receber_dados():
    data = request.get_json()
    print("DADOS RECEBIDOS:", data)
    status_code, result = create_notion_page(data)
    return jsonify(result), status_code



if __name__ == "__main__":
    app.run(debug=True)