"""
Fluent Wrapper - ANSYS Fluent API 封装
"""

import os
import json
from typing import Dict, Optional, List, Any
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


class FluentWrapper:
    """ANSYS Fluent API 封装类"""
    
    def __init__(self, config_path: str = "config/fluent_config.json"):
        """
        初始化 Fluent Wrapper
        
        Args:
            config_path: Fluent 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.fluent_path = os.getenv("FLUENT_PATH", self.config.get("fluent_path"))
        self.session = None
        self.solver = None
        
        logger.info("FluentWrapper initialized")
    
    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return {}
    
    def start_fluent(
        self, 
        dimension: str = "3d",
        precision: str = "dp",
        processor_count: int = 1,
        show_gui: bool = False
    ) -> Any:
        """
        启动 Fluent 会话
        
        Args:
            dimension: 维度 (2d, 3d)
            precision: 精度 (sp, dp)
            processor_count: 处理器数量
            show_gui: 是否显示 GUI
            
        Returns:
            Fluent 会话对象
        """
        logger.info(f"Starting Fluent {dimension} {precision} with {processor_count} processors...")
        
        try:
            import ansys.fluent.core as pyfluent
            
            self.session = pyfluent.launch_fluent(
                precision=precision,
                processor_count=processor_count,
                dimension=dimension.replace("d", ""),
                mode="solver",
                show_gui=show_gui,
                product_version=os.getenv("FLUENT_VERSION", "2024.1")
            )
            
            self.solver = self.session.solver
            logger.success("Fluent started successfully")
            
            return self.session
            
        except ImportError:
            logger.error("ansys-fluent-core not installed. Install with: pip install ansys-fluent-core")
            raise
        except Exception as e:
            logger.error(f"Failed to start Fluent: {e}")
            raise
    
    def stop_fluent(self):
        """停止 Fluent 会话"""
        if self.session:
            logger.info("Stopping Fluent session...")
            try:
                self.session.exit()
                logger.success("Fluent session stopped")
            except Exception as e:
                logger.error(f"Error stopping Fluent: {e}")
    
    def load_case(self, case_file: str) -> bool:
        """
        加载案例文件
        
        Args:
            case_file: 案例文件路径
            
        Returns:
            是否成功加载
        """
        if not self.session:
            logger.error("Fluent session not started")
            return False
        
        logger.info(f"Loading case file: {case_file}")
        
        try:
            self.solver.file.read_case(file_name=case_file)
            logger.success("Case file loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to load case file: {e}")
            return False
    
    def save_case(self, case_file: str) -> bool:
        """
        保存案例文件
        
        Args:
            case_file: 案例文件路径
            
        Returns:
            是否成功保存
        """
        if not self.session:
            logger.error("Fluent session not started")
            return False
        
        logger.info(f"Saving case file: {case_file}")
        
        try:
            self.solver.file.write_case(file_name=case_file)
            logger.success("Case file saved successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to save case file: {e}")
            return False
    
    def execute_tui_command(self, command: str) -> Any:
        """
        执行 TUI 命令
        
        Args:
            command: TUI 命令
            
        Returns:
            命令输出
        """
        if not self.session:
            logger.error("Fluent session not started")
            return None
        
        logger.info(f"Executing TUI command: {command}")
        
        try:
            # TUI 命令格式
            result = self.session.tui.execute(command)
            logger.success("TUI command executed")
            return result
        except Exception as e:
            logger.error(f"Failed to execute TUI command: {e}")
            return None
    
    def compile_udf(self, udf_file: str, lib_name: str = "libudf") -> bool:
        """
        编译 UDF
        
        Args:
            udf_file: UDF 文件路径
            lib_name: 库名称
            
        Returns:
            是否成功编译
        """
        if not self.session:
            logger.error("Fluent session not started")
            return False
        
        logger.info(f"Compiling UDF: {udf_file}")
        
        try:
            # 编译 UDF
            self.solver.tui.define.user_defined.compiled_functions.compile(
                lib_name=lib_name,
                src_file_name_list=[udf_file]
            )
            logger.success("UDF compiled successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to compile UDF: {e}")
            return False
    
    def load_udf(self, lib_name: str = "libudf") -> bool:
        """
        加载 UDF 库
        
        Args:
            lib_name: 库名称
            
        Returns:
            是否成功加载
        """
        if not self.session:
            logger.error("Fluent session not started")
            return False
        
        logger.info(f"Loading UDF library: {lib_name}")
        
        try:
            self.solver.tui.define.user_defined.compiled_functions.load(lib_name)
            logger.success("UDF library loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to load UDF library: {e}")
            return False
    
    def run_python_script(self, script_content: str) -> Any:
        """
        在 Fluent 中运行 Python 脚本
        
        Args:
            script_content: Python 脚本内容
            
        Returns:
            脚本输出
        """
        if not self.session:
            logger.error("Fluent session not started")
            return None
        
        logger.info("Running Python script in Fluent...")
        
        try:
            # 在 Fluent 上下文中执行
            result = exec(script_content, {"solver": self.solver, "session": self.session})
            logger.success("Python script executed")
            return result
        except Exception as e:
            logger.error(f"Failed to run Python script: {e}")
            return None
    
    def get_solution_data(self, variable: str) -> Optional[Dict]:
        """
        获取求解数据
        
        Args:
            variable: 变量名称
            
        Returns:
            数据字典
        """
        if not self.session:
            logger.error("Fluent session not started")
            return None
        
        logger.info(f"Getting solution data for: {variable}")
        
        try:
            # 获取数据的示例实现
            data = {}
            # 具体实现取决于 Fluent API
            logger.success("Solution data retrieved")
            return data
        except Exception as e:
            logger.error(f"Failed to get solution data: {e}")
            return None
