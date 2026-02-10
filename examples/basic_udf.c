#include "udf.h"

/**
 * 基础 UDF 示例: 抛物线速度分布
 * 
 * 此 UDF 定义了一个抛物线入口速度分布
 * 适用于管道流动等场景
 */

// 最大速度 (m/s)
#define VMAX 1.0

// 管道半径 (m)
#define RADIUS 0.05

/**
 * DEFINE_PROFILE 宏定义速度分布
 * 
 * @param thread - 边界线程
 * @param position - 位置索引 (对于速度: 0=x, 1=y, 2=z)
 */
DEFINE_PROFILE(parabolic_velocity, thread, position)
{
    real x[ND_ND];      // 位置向量
    real y, r;          // y 坐标和半径
    face_t f;           // 面索引
    
    // 遍历边界面
    begin_f_loop(f, thread)
    {
        // 获取面的质心坐标
        F_CENTROID(x, f, thread);
        
        // 计算距离中心线的半径
        // 假设流动沿 x 方向，管道中心在 y=0
        y = x[1];
        r = sqrt(y*y);
        
        // 抛物线速度分布: v(r) = vmax * (1 - (r/R)^2)
        // 仅在管道内部定义速度
        if (r <= RADIUS)
        {
            F_PROFILE(f, thread, position) = VMAX * (1.0 - (r*r)/(RADIUS*RADIUS));
        }
        else
        {
            F_PROFILE(f, thread, position) = 0.0;
        }
    }
    end_f_loop(f, thread)
}


/**
 * 使用说明:
 * 
 * 1. 编译此 UDF:
 *    - 在 Fluent 中: Define -> User-Defined -> Functions -> Compiled
 *    - 选择此文件并点击 Build
 * 
 * 2. 加载 UDF:
 *    - 点击 Load
 * 
 * 3. 应用到边界条件:
 *    - 选择入口边界
 *    - 设置速度类型为 "Velocity Inlet"
 *    - 在速度分量中选择 "parabolic_velocity"
 * 
 * 注意:
 * - 根据您的几何形状调整 RADIUS 值
 * - 根据您的坐标系调整位置索引
 * - 对于 2D 问题，使用 x[1] 作为 y 坐标
 * - 对于 3D 问题，可能需要同时考虑 x[1] 和 x[2]
 */
