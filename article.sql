/*
Navicat MySQL Data Transfer

Source Server         : scrapy
Source Server Version : 80019
Source Host           : localhost:3306
Source Database       : jianshu

Target Server Type    : MYSQL
Target Server Version : 80019
File Encoding         : 65001

Date: 2020-03-21 17:00:32
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `article`
-- ----------------------------
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article` (
  `id` int NOT NULL AUTO_INCREMENT,
  `article_id` varchar(20) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `content` longtext,
  `author` varchar(255) DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `pub_time` datetime DEFAULT NULL,
  `origin_url` varchar(255) DEFAULT NULL,
  `word_count` varchar(11) DEFAULT '00000000000',
  `read_count` varchar(11) DEFAULT '00000000000',
  `comment_count` varchar(11) DEFAULT '00000000000',
  `like_count` varchar(11) DEFAULT '00000000000',
  `subjects` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `creat_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of article_copy
-- ----------------------------
