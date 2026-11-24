import * as React from "react";
import { ListaAutomatica } from "@atendimento-lojas/ui";

export const OQueEAutomatico = () => (
  <ListaAutomatica itens={[
    { texto: "Responde a primeira mensagem do cliente com as boas-vindas da loja.", cor: "loja-baixa" },
    { texto: "Coloca a conversa na equipe da loja certa.", cor: "loja-praca" },
    { texto: "No Instagram, pergunta com qual loja o cliente quer falar (1 ou 2)." },
  ]} />
);
