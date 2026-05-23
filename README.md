# Turtlesim Image Drawing
---
Uma aplicação que é capaz de importar qualquer imagem que o usuário desejar e comandar de forma autônoma o Turtlesim para fazer o desenho do contorno da imagem. Isso é realizado por meio da pipeline Canny de detecção de bordas, com todas as transformações da imagem sendo realizadas por manipulação direta das matrizes por meio da biblioteca Numpy, sem uso de funções já existentes do OpenCV.

### Vídeo demonstrativo (WIP)

## Instruções de Execução

Clone esse repositório em seu dispositivo. Se desejar desenhar uma imagem específica, troque o arquivo de imagem em *src/turtle-artist/input.jpeg* (Deve ser uma .jpeg, daqui a pouco já implemento suporte para outros formatos). Na raiz do repositório, execute:
```bash
colcon build
```

Após o processo finalizar com sucesso, inicie o Turtlesim em outro terminal e execute o seguinte comando para iniciar o processo de desenho da imagem (Uma conexão estável é necessária para garantir a execução do programa sem erros!):

```bash
source install/setup.bash
ros2 run turtle-artist draw_image
```

## Documentação
(WIP)

Se você está lendo isso, eu ainda estou trabalhando nessa parte!! O código já está disponível e é funcional, mas peço que seja paciente com as demais partes, eu ainda não pude terminá-las.
