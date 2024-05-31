import os
import yaml
from mirai import *

from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
from pkg.command import entities
from pkg.command.operator import CommandOperator, operator_class
import typing

from plugins.vits.pkg.generate_voice import generate_audio

# 读取yaml配置文件
with open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)


ifVoice = config['voice_switch']
language = config['language']


# 增加指令
@operator_class(name="vits", help="vits开关 on/off/status", privilege=1)
class SwitchVoicePlugin(CommandOperator):

    # 控制语音合成的开关
    async def execute(self, context: entities.ExecuteContext) -> typing.AsyncGenerator[entities.CommandReturn, None]:
        global ifVoice
        global language

        if context.crt_params[0] == "on":
            self.ap.logger.info("启动语音合成")
            ifVoice = True
            yield entities.CommandReturn(text="启动语音合成")

        elif context.crt_params[0] == "off":
            self.ap.logger.info("关闭语音合成")
            ifVoice = False
            yield entities.CommandReturn(text="关闭语音合成")

        elif context.crt_params[0] == "status":
            if ifVoice:
                yield entities.CommandReturn(text="语音合成状态:已开启" + f"，当前语言为{language}")
            else:
                yield entities.CommandReturn(text="语音合成状态:已关闭")

        elif context.crt_params[0] == "language":

            reply = "语言列表：\n 中文  英文    日文"
                    

            yield entities.CommandReturn(text=reply.strip())

        elif context.crt_params[0] == "switch":
           
           language = context.crt_params[1]
           self.ap.logger.info(f"切换语音合成语言为{language}")
           yield entities.CommandReturn(text=f"切换语音合成语言为{language}")

        elif context.crt_params[0] == "帮助":
            yield entities.CommandReturn(text="vits插件支持的指令有：\n"
                                              "!vits on\n"
                                              "!vits off\n"
                                              "!vits status\n"
                                              "!vits language\n"
                                              "!vits switch\n"
                                              "!vits help\n")

        else:
            yield entities.CommandReturn(error="无效指令，请输入\"!vits help\"查看帮助")


# 注册插件
@register(name="vits", description="一个语音插件", version=".1", author="logos")
class VoicePlugin(BasePlugin):
    # 插件加载时触发
    def __init__(self, host: APIHost):
        # 清空同目录的audio_temp文件夹下的所有文件
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "audio_temp"))
        
        if os.path.exists(base_path):
            for file in os.listdir(base_path):
                os.remove(os.path.join(base_path, file))
        pass

    # 当消息回复时触发
    @handler(NormalMessageResponded)
    async def text_to_voice(self, ctx: EventContext):
        #print(1111111111111111)
        global ifVoice
        global language
        # 如果语音开关开启
        if ifVoice:
            # 获取回复内容
            res_text = ctx.event.response_text

            self.ap.logger.info(f"使用角色生成回复语音")
            # 生成语音
            result = generate_audio(res_text, language)
            
            if result:
                # 回复语音消息
                ctx.add_return("reply", [Voice(path=str(result))])

                # 删除生成的silk语音文件
                #os.remove(result)
            #print(121,result)
            

