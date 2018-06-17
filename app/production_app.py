from app.application import main
from settings import production

if __name__ == '__main__':
    config = vars(production)
    main(config)
