from app.application import main
from settings import local

if __name__ == '__main__':
    config = vars(local)
    main(config)