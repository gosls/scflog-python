import json, os, time
from plumbum import cli
from ws4py.client.threadedclient import WebSocketClient


class CG_Client(WebSocketClient):

    def opened(self):
        print("实时日志开启 ... ")

    def closed(self, code, reason=None):
        print("实时日志关闭。", code, reason)

    def received_message(self, resp):
        print(time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time())), ": ", resp)


class ScfPythonLogs(cli.Application):
    VERSION = "0.0.5"
    # def main(self):
    #     print("欢迎使用腾讯云SCF Python实时日志查看工具")
    #     print("1: 您需要通过scflogs set来设置websocket等信息，例如：")
    #     print("\t scflogs set -w ws://service-e97dc5uu-1256773370.gz.apigw.tencentcs.com/test/python_real_time_logs")
    #     print("1: 通过scflogs logs指令获取实时日志功能，例如：")
    #     print("\t scflogs logs -n MyFuntionName -ns Namesapce -r Region")


@ScfPythonLogs.subcommand("set")
class ScfPythonLogsSet(cli.Application):
    '''
        设置Websocket地址等相关信息。
    '''

    websocket = cli.SwitchAttr(["w", "websocket"], str, help="Websocket地址")
    region = cli.SwitchAttr(["r", "region"], help="常用函数的区域（非必选，默认ap-guangzhou）")
    namespace = cli.SwitchAttr(["ns", "namespace"], help="常用函数的命名空间（非必选，默认default）")

    def main(self):
        configure = {
            "websocket": "",
            "region": "ap-guangzhou",
            "namespace": "default"
        }
        pathData = os.path.join(os.path.expanduser('~'), ".scf_python_logs")
        if os.path.exists(pathData):
            try:
                with open(pathData) as f:
                    configure = json.loads(f.read())
            except:
                pass

        configure = {
            "websocket": self.websocket if self.websocket else configure["websocket"],
            "region": self.region if self.region else configure["region"],
            "namespace": self.namespace if self.namespace else configure["namespace"],
        }
        with open(pathData, 'w') as f:
            f.write(json.dumps(configure))
        print("设置成功")
        for eveKey, eveValue in configure.items():
            if eveValue:
                print("\t%s: %s" % (eveKey, eveValue))


@ScfPythonLogs.subcommand("logs")
class ScfPythonLogsLogs(cli.Application):
    '''
        开启实时日志查看功能
    '''
    funtionName = cli.SwitchAttr(["n", "name"], help="函数名称")
    region = cli.SwitchAttr(["r", "region"], help="该函数所在区域，如果不写则以set中的region为准，默认ap-guangzhou")
    namespace = cli.SwitchAttr(["ns", "namespace"], help="该函数所处命名空间，如果不写则以set中的region为准，默认default")

    def main(self):
        pathData = os.path.join(os.path.expanduser('~'), ".scf_python_logs")
        if os.path.exists(pathData):
            if not self.funtionName:
                raise Exception("函数名称必须填写")
            with open(pathData) as f:
                configure = json.loads(f.read())
            websocket = configure.get("websocket", None)
            if not websocket:
                raise Exception("使用前请通过set指令设置websocket地址")
            namespace = self.namespace if self.namespace else configure.get("namespace", "default")
            region = self.region if self.region else configure.get("region", "ap-guangzhou")
            websocketUrl = '%s?name=%s&namespace=%s&region=%s' % (websocket, self.funtionName, namespace, region)
            ws = None
            try:
                ws = CG_Client(websocketUrl)
                ws.connect()
                ws.run_forever()
            except Exception as e:
                if ws:
                    ws.close()
        else:
            raise Exception("使用前请通过set指令设置websocket地址")


@ScfPythonLogs.subcommand("init")
class ScfPythonLogsInit(cli.Application):
    '''
        在项目中执行可以将中间件打入项目中
    '''

    def main(self):
        loggingPath = os.path.abspath(__file__).replace('cmds.py', 'logging_mid.py')
        logsPath = os.path.abspath(__file__).replace('cmds.py', 'logs_mid.py')
        with open(os.path.join(os.getcwd(), "logging.py"),"wb") as wf:
            with open(loggingPath, "rb") as rf:
                wf.write(rf.read())
        with open(os.path.join(os.getcwd(), "logs.py"),"wb") as wf:
            with open(logsPath, "rb") as rf:
                wf.write(rf.read())


if __name__ == "__main__":
    ScfPythonLogs.run()
