import subprocess
import threading
import time
import queue
import re


class AdvancedWinDbgInterface:
    def __init__(self, windbg_path="windbg.exe"):
        self.windbg_path = windbg_path
        self.process = None
        self.output_queue = queue.Queue()
        self.error_queue = queue.Queue()
        self.command_queue = queue.Queue()
        self.is_running = False
        self.output_callback = None
        self.error_callback = None

    def set_callbacks(self, output_callback=None, error_callback=None):
        """设置回调函数"""
        self.output_callback = output_callback
        self.error_callback = error_callback

    def start(self, target=None, args=None):
        """启动 WinDbg"""
        cmd_args = [self.windbg_path]

        if args:
            cmd_args.extend(args)

        if target:
            if isinstance(target, int):
                cmd_args.extend(["-p", str(target)])  # 附加到进程
            else:
                cmd_args.extend(["-z", target,"-c",".logopen 3.log"])  # 打开转储文件

        try:
            self.process = subprocess.Popen(
                cmd_args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0,
                encoding="utf-8",
                errors='ignore',
                universal_newlines=True
            )

            self.is_running = True

            # 启动处理线程
            threading.Thread(target=self._handle_stdout, daemon=True).start()
            threading.Thread(target=self._handle_stderr, daemon=True).start()
            threading.Thread(target=self._handle_commands, daemon=True).start()

            print("WinDbg started successfully")
            return True

        except Exception as e:
            print(f"Failed to start WinDbg: {e}")
            return False

    def _handle_stdout(self):
        """处理标准输出"""
        while self.is_running and self.process:
            try:
                line = self.process.stdout.readline()
                if line:
                    self.output_queue.put(line.strip())
                    if self.output_callback:
                        self.output_callback(line.strip())
            except Exception as e:
                if self.is_running:
                    print(f"Error reading stdout: {e}")
                break

    def _handle_stderr(self):
        """处理标准错误"""
        while self.is_running and self.process:
            try:
                line = self.process.stderr.readline()
                if line:
                    self.error_queue.put(line.strip())
                    if self.error_callback:
                        self.error_callback(line.strip())
            except Exception as e:
                if self.is_running:
                    print(f"Error reading stderr: {e}")
                break

    def _handle_commands(self):
        """处理命令队列"""
        while self.is_running:
            try:
                if not self.command_queue.empty():
                    command = self.command_queue.get(timeout=0.1)
                    self._send_command_internal(command)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error handling commands: {e}")

    def _send_command_internal(self, command):
        """内部发送命令方法"""
        try:
            self.process.stdin.write(command + '\n')
            self.process.stdin.flush()
        except Exception as e:
            print(f"Failed to send command '{command}': {e}")

    def send_command(self, command, async_send=True):
        """发送命令"""
        if not self.is_running or not self.process:
            raise Exception("WinDbg is not running")

        if async_send:
            self.command_queue.put(command)
        else:
            self._send_command_internal(command)

    def get_output(self, timeout=5):
        """获取输出"""
        lines = []
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                line = self.output_queue.get(timeout=0.1)
                lines.append(line)
            except queue.Empty:
                break

        return '\n'.join(lines)

    def get_error(self, timeout=5):
        """获取错误输出"""
        lines = []
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                line = self.error_queue.get(timeout=0.1)
                lines.append(line)
            except queue.Empty:
                break

        return '\n'.join(lines)

    def execute_command(self, command, timeout=10):
        """执行命令并等待结果"""
        # 清空现有输出
        while not self.output_queue.empty():
            try:
                self.output_queue.get_nowait()
            except queue.Empty:
                break

        # 发送命令
        self.send_command(command)

        # 等待结果
        # time.sleep(0.5)  # 给命令一些执行时间

        # 获取输出
        result = self.get_output(timeout)
        error = self.get_error(1)

        if error:
            print(f"Command error: {error}")

        return result

    def stop(self):
        """停止 WinDbg"""
        self.is_running = False
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()


# 使用示例
def output_handler(line):
    print(f"[WinDbg Output] {line}")


def error_handler(line):
    print(f"[WinDbg Error] {line}")


if __name__ == "__main__":
    # 创建高级接口
    windbg = AdvancedWinDbgInterface(
        r"C:\Users\15319\AppData\Local\Microsoft\WindowsApps\kdX86.exe"
    )

    # 设置回调
    windbg.set_callbacks(output_handler, error_handler)
    dump_file = r"D:\0_LOG_VIP\11\0x9f_3_Disk_FastBoot\MEMORY.DMP"
    # 启动 WinDbg
    if windbg.start(target=dump_file):
        # time.sleep(3)  # 等待初始化

        # 执行一些调试命令
        commands = [
            # "-y", f'{SYMBOL_PATH}',
            "!analyze  -v",
           ".logclose",
            "qqd"
        ]

        for cmd in commands:
            print(f"Executing: {cmd}")
            cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
            if result:
                print(f"Result:\n{result}")
            print("-" * 50)
            # time.sleep(1)

        # 保持运行
        try:
            time.sleep(30)
        except KeyboardInterrupt:
            print("Stopping...")

        windbg.stop(path_dir)