# Turtlesim Image Drawing
---
Uma aplicação que é capaz de importar qualquer imagem que o usuário desejar e comandar de forma autônoma o Turtlesim para fazer o desenho do contorno da imagem. Isso é realizado por meio da pipeline Canny de detecção de bordas, com todas as transformações da imagem sendo realizadas por manipulação direta das matrizes por meio da biblioteca Numpy, sem uso de funções já existentes do OpenCV.

<img src='assets/demo.gif'>

## [Vídeo de demonstração básica](https://drive.google.com/file/d/1wbNXbA-2_1UmZSjmlqh7RT_y6LZbaexj/view?usp=sharing)

# Instruções de Execução

Clone esse repositório em seu dispositivo. Na raiz do repositório, execute:
```bash
colcon build
```

Após o processo finalizar com sucesso, inicie o Turtlesim em outro terminal e execute o seguinte comando para iniciar o processo de desenho da imagem (Uma conexão estável é necessária para garantir a execução do programa sem erros!):

```bash
source install/setup.bash
ros2 run turtle-artist draw_image
```

A aplicação abrirá uma interface para que selecione uma imagem do seu computador para ser desenhada. Se não selecionar nenhuma, uma imagem padrão (o cachorro) será utilizada.

# Documentação
(WIP)

Se você está lendo isso, eu ainda estou trabalhando nessa parte!! O código já está disponível e é funcional, mas peço que seja paciente com as demais partes, eu ainda não pude terminá-las.
