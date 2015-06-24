# OP
#建表

CREATE TABLE `iptables` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `host` varchar(255) DEFAULT NULL,
  `ip` varchar(255) DEFAULT NULL,
  `iptables` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8 | 
