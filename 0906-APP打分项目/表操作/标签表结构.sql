/*
Navicat MySQL Data Transfer

Source Server         : hive
Source Server Version : 80011
Source Host           : localhost:3306
Source Database       : tags

Target Server Type    : MYSQL
Target Server Version : 80011
File Encoding         : 65001

Date: 2018-09-10 14:50:11
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for tag_1101_sex
-- ----------------------------
DROP TABLE IF EXISTS `tag_1101_sex`;
CREATE TABLE `tag_1101_sex` (
  `source_id` varchar(100) DEFAULT NULL,
  `id_type` varchar(100) DEFAULT NULL,
  `id` varchar(100) DEFAULT NULL,
  `tag_domain` varchar(100) DEFAULT NULL,
  `tag_id` varchar(100) DEFAULT NULL,
  `tag_path` varchar(100) DEFAULT NULL,
  `tag_value_type` varchar(100) DEFAULT NULL,
  `tag_value` varchar(100) DEFAULT NULL,
  `updatetime` varchar(100) DEFAULT NULL  
) partitioned by (`dt` varchar(100)) ;