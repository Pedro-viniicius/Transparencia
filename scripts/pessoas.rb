# Cria (ou atualiza) as pessoas da conta, já confirmadas e com senha, sem depender de e-mail.
# Uso: docker compose exec -T chatwoot bundle exec rails runner - < scripts/pessoas.rb
# Lê PESSOAS_JSON (lista de {nome, email, papel, senha}) e ADMIN_EMAIL do ambiente.
# Imprime em JSON: {account_id, admin_token, pessoas: [{email, id, papel}]}.
require 'json'

admin = User.find_by!(email: ENV.fetch('ADMIN_EMAIL'))
account = admin.accounts.first or abort('administrador sem conta')

saida = JSON.parse(ENV.fetch('PESSOAS_JSON')).map do |p|
  user = User.find_or_initialize_by(email: p['email'])
  novo = user.new_record?
  user.name = p['nome']
  user.display_name = p['nome']
  if novo
    user.password = p['senha']
    user.password_confirmation = p['senha']
    user.skip_confirmation!
  end
  user.save!
  au = AccountUser.find_or_initialize_by(account: account, user: user)
  au.role = p['papel']
  au.save!
  { email: user.email, id: user.id, papel: au.role, novo: novo }
end

puts JSON.generate(account_id: account.id, admin_token: admin.access_token.token, pessoas: saida)
