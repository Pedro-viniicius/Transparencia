import * as React from "react";
import { ListaPassos } from "@atendimento-lojas/ui";

export const GuiaDaAtendente = () => (
  <ListaPassos passos={[
    { titulo: "Fique Online", texto: "Ao entrar, confira se seu status está Online. Conversa nova só vai para quem está online." },
    { titulo: "Você vê a sua loja", texto: "Cada atendente vê só as conversas da própria loja. O dono e a esposa veem as duas." },
    { titulo: "Responda pela conversa", texto: "O cliente recebe no WhatsApp com o seu nome em cima da mensagem." },
    { titulo: "Terminou? Resolva", texto: "Clique em Resolver. Se o cliente escrever de novo, a conversa aparece outra vez." },
  ]} />
);
export const TresPassos = () => (
  <ListaPassos passos={[
    { titulo: "Abra o WhatsApp da loja", texto: "No celular com o chip da loja." },
    { titulo: "Dispositivos conectados", texto: "Toque em Conectar dispositivo." },
    { titulo: "Escaneie o código", texto: "Ele se renova sozinho a cada 5 segundos." },
  ]} />
);
