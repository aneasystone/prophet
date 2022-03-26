# prophet

stock predictor

## 安装依赖

```
pip install tushare pandas sqlalchemy pymysql
```

然后安装 `ta-lib`，[参考这里](https://blog.csdn.net/weixin_40327641/article/details/81076438)。

Linux 环境下：

```
# tar -xzvf ta-lib-0.4.0-src.tar.gz
# cd ta-lib
# ./configure --prefix=/usr
# make && make install
# cd ..
# pip install TA-Lib
```

Windows 环境下可以直接安装 whl 文件：

```
# pip install ./TA_Lib-0.4.19-cp37-cp37m-win_amd64.whl
```

## 准备数据库

```
/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`stock` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `stock`;

/*Table structure for table `daily` */

DROP TABLE IF EXISTS `daily`;

CREATE TABLE `daily` (
  `ts_code` varchar(32) DEFAULT NULL,
  `trade_date` varchar(32) DEFAULT NULL,
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  `pre_close` double DEFAULT NULL,
  `change` double DEFAULT NULL,
  `pct_chg` double DEFAULT NULL,
  `vol` double DEFAULT NULL,
  `amount` double DEFAULT NULL,
  KEY `ts_code_trade_date` (`ts_code`,`trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Table structure for table `stock_basic` */

DROP TABLE IF EXISTS `stock_basic`;

CREATE TABLE `stock_basic` (
  `ts_code` varchar(32) DEFAULT NULL,
  `symbol` varchar(32) DEFAULT NULL,
  `name` varchar(32) DEFAULT NULL,
  `area` varchar(32) DEFAULT NULL,
  `industry` varchar(32) DEFAULT NULL,
  `list_date` varchar(32) DEFAULT NULL,
  KEY `ts_code` (`ts_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `daily_basic`;

CREATE TABLE `daily_basic` (
  `ts_code` varchar(32) DEFAULT NULL,
  `trade_date` varchar(32) DEFAULT NULL,
  `close` double DEFAULT NULL,
  `turnover_rate` double DEFAULT NULL,
  `turnover_rate_f` double DEFAULT NULL,
  `volume_ratio` double DEFAULT NULL,
  `pe` double DEFAULT NULL,
  `pe_ttm` double DEFAULT NULL,
  `pb` double DEFAULT NULL,
  `ps` double DEFAULT NULL,
  `ps_ttm` double DEFAULT NULL,
  `dv_ratio` double DEFAULT NULL,
  `dv_ttm` double DEFAULT NULL,
  `total_share` double DEFAULT NULL,
  `float_share` double DEFAULT NULL,
  `free_share` double DEFAULT NULL,
  `total_mv` double DEFAULT NULL,
  `circ_mv` double DEFAULT NULL,
  KEY `ts_code_trade_date` (`ts_code`,`trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `money_flow`;

CREATE TABLE `money_flow` (
  `ts_code` varchar(32) DEFAULT NULL,
  `trade_date` varchar(32) DEFAULT NULL,
  `buy_sm_vol` bigint(20) DEFAULT NULL,
  `buy_sm_amount` double DEFAULT NULL,
  `sell_sm_vol` bigint(20) DEFAULT NULL,
  `sell_sm_amount` double DEFAULT NULL,
  `buy_md_vol` bigint(20) DEFAULT NULL,
  `buy_md_amount` double DEFAULT NULL,
  `sell_md_vol` bigint(20) DEFAULT NULL,
  `sell_md_amount` double DEFAULT NULL,
  `buy_lg_vol` bigint(20) DEFAULT NULL,
  `buy_lg_amount` double DEFAULT NULL,
  `sell_lg_vol` bigint(20) DEFAULT NULL,
  `sell_lg_amount` double DEFAULT NULL,
  `buy_elg_vol` bigint(20) DEFAULT NULL,
  `buy_elg_amount` double DEFAULT NULL,
  `sell_elg_vol` bigint(20) DEFAULT NULL,
  `sell_elg_amount` double DEFAULT NULL,
  `net_mf_vol` bigint(20) DEFAULT NULL,
  `net_mf_amount` double DEFAULT NULL,
  KEY `ts_code_trade_date` (`ts_code`,`trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
```

## 初始化数据

```
$ python updator.py
```

## 运行

在 `strategy_factory` 中选择策略，然后执行：

```
$ python main.py
```
