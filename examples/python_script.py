"""
使用 PyFluent 的示例脚本
演示如何通过 Python 控制 ANSYS Fluent
"""

import sys
from pathlib import Path

# 导入 Fluent 集成模块
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fluent_integration import FluentWrapper


def main():
    """主函数"""
    print("="*50)
    print("  ANSYS Fluent Python 脚本示例")
    print("="*50)
    
    # 初始化 Fluent Wrapper
    print("\n初始化 Fluent Wrapper...")
    wrapper = FluentWrapper()
    
    # 启动 Fluent
    print("\n启动 Fluent 会话...")
    try:
        session = wrapper.start_fluent(
            dimension="3d",
            precision="dp",
            processor_count=2,
            show_gui=False
        )
        
        print("✅ Fluent 启动成功!")
        
        # 获取 solver 对象
        solver = session.solver
        
        # 示例: 设置模型
        print("\n设置计算模型...")
        # solver.setup.models.energy.enabled = True
        # solver.setup.models.viscous.model = "k-epsilon"
        
        print("✅ 模型设置完成!")
        
        # 示例: 定义材料
        print("\n定义材料...")
        # air = solver.setup.materials.fluid["air"]
        # air.density.value = 1.225
        
        print("✅ 材料定义完成!")
        
        # 示例: 设置边界条件
        print("\n设置边界条件...")
        # inlet = solver.setup.boundary_conditions.velocity_inlet["inlet"]
        # inlet.velocity.value = 10
        
        print("✅ 边界条件设置完成!")
        
        # 示例: 初始化
        print("\n初始化流场...")
        # solver.solution.initialization.initialize_flow_field()
        
        print("✅ 流场初始化完成!")
        
        # 示例: 运行计算
        print("\n运行计算...")
        # solver.solution.run_calculation.iterate(number_of_iterations=100)
        
        print("✅ 计算完成!")
        
        # 停止 Fluent
        print("\n停止 Fluent 会话...")
        wrapper.stop_fluent()
        print("✅ Fluent 已停止!")
        
    except ImportError:
        print("❌ ansys-fluent-core 未安装")
        print("   安装命令: pip install ansys-fluent-core")
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    print("\n" + "="*50)
    print("  脚本执行完成")
    print("="*50)


if __name__ == "__main__":
    main()
