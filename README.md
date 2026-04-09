🚀 Python Automation Scripts

Repositório contendo scripts em Python para automação de tarefas operacionais, manutenção de ambientes e rotinas administrativas.

📌 Objetivo

Centralizar scripts reutilizáveis para:

🧹 Limpeza automática de arquivos (logs, temporários, uploads)
📊 Rotinas de monitoramento
🔄 Automação de processos operacionais
⚙️ Scripts de suporte para infraestrutura (IIS, serviços, arquivos)
🛠️ Ferramentas auxiliares para troubleshooting

⚙️ Requisitos
Python 3.10+
Windows Server / Linux
Permissões adequadas de leitura/escrita nos diretórios

Instale as dependências:

pip install -r requirements.txt
▶️ Como Executar
🔹 Execução simples
python scripts/limpeza_automatica_publicados.py
🔹 Execução com parâmetros
python scripts/limpeza_automatica_publicados.py --days 2 --log-file logs/limpeza.log
🔹 Modo simulação (Dry Run)
python scripts/limpeza_automatica_publicados.py --dry-run
🧹 Exemplo de Uso

Remover arquivos com mais de 2 dias:

python scripts/limpeza_automatica_publicados.py --days 2

Saída esperada:

[INFO] Removendo arquivo: log_20260401.txt
[INFO] Removendo arquivo: imagem_20260401.jpg
[OK] Limpeza concluída com sucesso
🛡️ Boas Práticas
Sempre utilize --dry-run antes de executar em produção
Configure logs para auditoria
Restrinja permissões de execução
Evite rodar scripts diretamente como administrador/root sem necessidade
Versione alterações no repositório
⏰ Agendamento
Windows (Task Scheduler)
Criar tarefa agendada
Ação:
python C:\Scripts\limpeza_automatica_publicados.py --days 2
Linux (Crontab)
0 2 * * * /usr/bin/python3 /scripts/limpeza_automatica_publicados.py --days 2
🔧 Configuração

Exemplo de config.yaml:

paths:
  - D:/Publicados/
  - C:/Logs/

retention_days: 2

log_file: logs/limpeza.log
📊 Logs

Os logs são armazenados em:

logs/limpeza.log

Exemplo:

2026-04-09 02:00:01 [INFO] Iniciando limpeza
2026-04-09 02:00:02 [INFO] Arquivo removido: log_20260405.txt
2026-04-09 02:00:03 [INFO] Finalizado com sucesso
🚨 Segurança
Não versionar arquivos sensíveis (usar .gitignore)
Evitar hardcode de caminhos críticos
Validar entradas via CLI
Implementar tratamento de exceções
📦 Roadmap
 Interface web para execução
 Integração com Zabbix / Prometheus
 Notificações via e-mail/Slack
 Execução distribuída via Kubernetes Jobs
 Integração com logs centralizados (Graylog)
🤝 Contribuição
Fork do projeto
Crie uma branch (feature/nova-funcionalidade)
Commit suas alterações
Push para o repositório
Abra um Pull Request
📄 Licença

Este projeto está sob a licença MIT.

👨‍💻 Autor

Desenvolvido por Alan Goulart
Especialista em Infraestrutura, DevOps e Observabilidade Industrial
