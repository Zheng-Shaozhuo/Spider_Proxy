/*
Navicat MySQL Data Transfer

Source Server         : aliyun
Source Server Version : 50556
Source Host           : 47.100.61.41:3306
Source Database       : vv_spider

Target Server Type    : MYSQL
Target Server Version : 50556
File Encoding         : 65001

Date: 2018-07-18 12:46:52
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `proxies`
-- ----------------------------
DROP TABLE IF EXISTS `proxies`;
CREATE TABLE `proxies` (
  `id` int(11) NOT NULL DEFAULT '0' COMMENT '主键',
  `ip` varchar(15) NOT NULL DEFAULT '0.0.0.0' COMMENT 'IP',
  `port` int(11) NOT NULL DEFAULT '80' COMMENT '端口',
  `valid` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否有效',
  `memo` varchar(256) NOT NULL COMMENT '备注',
  `last_check_timestamp` int(11) NOT NULL DEFAULT '0' COMMENT '最后检查时间',
  `created_at` int(11) NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of proxies
-- ----------------------------
