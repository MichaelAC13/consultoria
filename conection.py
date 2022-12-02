class connection():
    def createmercadorias(): 
        createmercadorias = """
        USE `consultoria`;
        CREATE TABLE IF NOT EXISTS `mercadorias`(
        `id` int NOT NULL AUTO_INCREMENT,
        `descricao` varchar(450) NOT NULL,
        `ncm` varchar(200) DEFAULT NULL,
        `pisecofins` varchar(450) DEFAULT NULL,
        `setor` varchar(450) DEFAULT NULL,
        `icms` varchar(450) DEFAULT NULL,
        `status` varchar(100) DEFAULT NULL,
        `dtupdate` datetime DEFAULT NULL,
        `fornecedores` varchar(15000) DEFAULT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `id_UNIQUE` (`id`)
        );
        """
        return createmercadorias

    def createfornecedores(): 
        createmercadorias = """
        USE `consultoria`;
        CREATE TABLE IF NOT EXISTS `fornecedor`(
        `id` int NOT NULL AUTO_INCREMENT,
        `cnpj` varchar(450) NOT NULL,
        `fornecedor` varchar(2000) DEFAULT NULL,
        `atacado` varchar(100) DEFAULT NULL,
        `ie` varchar(20) DEFAULT NULL,
        `estado` varchar(300) DEFAULT NULL,
        `cidade` varchar(300) DEFAULT NULL,
        `logradouro` varchar(500) DEFAULT NULL,
        `numero` varchar(30) DEFAULT NULL,
        `bairro` varchar(300) DEFAULT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `id_UNIQUE` (`id`),
        UNIQUE KEY `cnpj_UNIQUE` (`cnpj`)
        );
        """
        return createmercadorias

    def createusers():
        createusers = """
        USE `consultoria`;
        CREATE TABLE  IF NOT EXISTS `users`(
        `id` int NOT NULL AUTO_INCREMENT,
        `email` varchar(450) NOT NULL,
        `hashcode` varchar(450) DEFAULT NULL,
        `name` varchar(450) DEFAULT NULL,
        `status` varchar(1) DEFAULT NULL,
        `master` varchar(1) DEFAULT NULL,
        `dtupdate` datetime DEFAULT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `id_UNIQUE` (`id`),
        UNIQUE KEY `email_UNIQUE` (`email`)
        );
        """
        return createusers
