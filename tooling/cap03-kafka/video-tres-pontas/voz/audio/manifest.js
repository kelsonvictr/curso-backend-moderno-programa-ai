// Áudios locais gerados via ElevenLabs. Sem credenciais.
window.VOZES = {
  "B01": [
    {
      "file": "llm-526b250190990eda5e10.mp3",
      "role": "LLM",
      "text": "Fase dois: as três pontas do mesão. O tópico agora tem três partições.",
      "duration": 7.105306
    }
  ],
  "B02": [
    {
      "file": "llm-5e37633880d4b5935089.mp3",
      "role": "LLM",
      "text": "Cada partição é uma ponta da mesa, com seus próprios registros e offsets.",
      "duration": 5.572789
    }
  ],
  "B03": [
    {
      "file": "lia-fd20ecf0238489c97609.mp3",
      "role": "LIA",
      "text": "E como o Kafka escolhe a ponta de cada pedido?",
      "duration": 2.739955
    }
  ],
  "B04": [
    {
      "file": "llm-06ceb7bd4a4c5566d32c.mp3",
      "role": "LLM",
      "text": "Pela chave. Mesma chave, mesma partição. Aqui, a chave é o número do pedido.",
      "duration": 6.780227
    }
  ],
  "B05": [
    {
      "file": "beto-6fec75967d815564f57d.mp3",
      "role": "BETO",
      "text": "Pedido A: criado, pago, enviado. Tudo na partição um, em ordem. Perfeito!",
      "duration": 4.92263
    }
  ],
  "B06": [
    {
      "file": "llm-c81f6f311a1d58a8cff5.mp3",
      "role": "LLM",
      "text": "Agora, sem chave. O produtor espalha os registros pelas pontas.",
      "duration": 4.643991
    }
  ],
  "B07": [
    {
      "file": "lia-d96ba410b545854f3fbf.mp3",
      "role": "LIA",
      "text": "Eita! Eu li \"A enviado\" antes de o Beto ler \"A pago\"!",
      "duration": 3.854512
    }
  ],
  "B08": [
    {
      "file": "beto-00497416f8e01d9cd720.mp3",
      "role": "BETO",
      "text": "Enviou antes de pagar? Isso vai dar problema!",
      "duration": 2.321995
    }
  ],
  "B09": [
    {
      "file": "llm-f2f0371f78ea6499b9ff.mp3",
      "role": "LLM",
      "text": "Ordem só existe dentro da partição. Por isso a chave importa.",
      "duration": 4.226032
    }
  ],
  "B10": [
    {
      "file": "lia-33fea846b4250974eae8.mp3",
      "role": "LIA",
      "text": "E esse quarto colega aí, parado?",
      "duration": 2.043356
    }
  ],
  "B11": [
    {
      "file": "llm-b96428c18907d7e98a5c.mp3",
      "role": "LLM",
      "text": "Três partições, quatro consumidores no mesmo grupo. Um fica de reserva, sem partição.",
      "duration": 6.130068
    }
  ]
};
