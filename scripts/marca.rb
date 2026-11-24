# Marca da instalação (nome e logos) e avatar de cada caixa. Idempotente.
# Rodado pelo configurar.py: docker compose exec -T -e MARCA_JSON=... chatwoot rails runner -
require 'json'
require 'base64'
require 'digest'
require 'stringio'

dados = JSON.parse(ENV.fetch('MARCA_JSON'))

dados.fetch('configs').each do |nome, valor|
  config = InstallationConfig.find_or_initialize_by(name: nome)
  next if config.persisted? && config.value == valor

  config.value = valor
  config.save!
end
GlobalConfig.clear_cache if GlobalConfig.respond_to?(:clear_cache)

trocados = []
dados.fetch('avatares').each do |a|
  inbox = Inbox.find(a.fetch('inbox_id'))
  bytes = Base64.strict_decode64(a.fetch('base64'))
  next if inbox.avatar.attached? && inbox.avatar.blob.checksum == Digest::MD5.base64digest(bytes)

  inbox.avatar.attach(io: StringIO.new(bytes), filename: a.fetch('arquivo'), content_type: 'image/png')
  trocados << inbox.name
end

puts JSON.generate(ok: true, avatares_trocados: trocados)
