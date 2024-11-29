#include "dl_model_base.hpp"
#include "esp_log.h"
#include "esp_timer.h"
#include "fbs_loader.hpp"
#include "test_image.hpp"  // 这个是我们要创建的图像数据头文件
#include <vector>

static const char *TAG = "GESTURE_RECOGNITION";

using namespace dl;

// 手势标签定义
const char* GESTURE_LABELS[] = {
    "palm", "l", "fist", "thumb", "index", "ok", "c", "down"
};
const int NUM_CLASSES = 8;

// 准备模型输入数据
TensorBase* prepare_input_tensor() {
    // 使用来自 test_image.hpp 的预处理数据
    // 假设数据已经是量化后的 int8 格式
    TensorBase* input_tensor = new TensorBase(
        {1, 1, 96, 96},              // 输入形状 [batch, channel, height, width]
        test_image_data,             // 来自 test_image.hpp 的数据指针
        -7,                          // exponent，需要根据实际量化参数调整
        dl::DATA_TYPE_INT8,          // 数据类型
        false,                       // 是否需要拷贝数据
        MALLOC_CAP_SPIRAM           // 内存分配标志
    );
    return input_tensor;
}

// 计算和输出置信度
void print_confidences(TensorBase* output_tensor) {
    if (!output_tensor) {
        ESP_LOGE(TAG, "Invalid output tensor");
        return;
    }

    // 获取输出数据
    int8_t* output_data = static_cast<int8_t*>(output_tensor->get_element_ptr());
    float scale = std::pow(2, output_tensor->exponent);  // 反量化比例

    // 确保输出大小正确
    if (output_tensor->get_size() != NUM_CLASSES) {
        ESP_LOGE(TAG, "Unexpected output size: %d", output_tensor->get_size());
        return;
    }

    // 计算 softmax 和置信度
    float max_val = -INFINITY;
    for (int i = 0; i < NUM_CLASSES; i++) {
        float val = output_data[i] * scale;
        if (val > max_val) max_val = val;
    }

    float sum = 0;
    std::vector<float> confidences(NUM_CLASSES);
    for (int i = 0; i < NUM_CLASSES; i++) {
        float val = std::exp((output_data[i] * scale) - max_val);
        confidences[i] = val;
        sum += val;
    }

    // 输出每个类别的置信度
    ESP_LOGI(TAG, "Gesture Recognition Results:");
    for (int i = 0; i < NUM_CLASSES; i++) {
        float confidence = confidences[i] / sum;
        ESP_LOGI(TAG, "%s: %.2f%%", GESTURE_LABELS[i], confidence * 100);
    }
}

extern "C" void app_main(void)
{
    ESP_LOGI(TAG, "Starting gesture recognition...");

    int64_t start_time = esp_timer_get_time();  // 模型加载开始时间

    // 创建模型实例
    Model* model = new Model("model", fbs::MODEL_LOCATION_IN_FLASH_PARTITION);
    if (!model) {
        ESP_LOGE(TAG, "Failed to create model");
        return;
    }

    int64_t load_time = esp_timer_get_time();   // 模型加载结束时间
    ESP_LOGI(TAG, "Model loaded in %lld ms", (load_time - start_time) / 1000);

    // 准备输入数据
    TensorBase* input_tensor = prepare_input_tensor();
    if (!input_tensor) {
        ESP_LOGE(TAG, "Failed to prepare input tensor");
        delete model;
        return;
    }

    // 构建输入map
    std::map<std::string, TensorBase*> inputs;
    inputs["input"] = input_tensor;  // 注意：这里的 "input" 需要与模型定义匹配

    // 运行推理
    ESP_LOGI(TAG, "Running inference...");

    size_t free_mem_before = heap_caps_get_free_size(MALLOC_CAP_SPIRAM);
    ESP_LOGI(TAG, "Free memory before inference: %u bytes", free_mem_before);
    int64_t inference_start = esp_timer_get_time();  // 推理开始时间

    model->run(inputs);

    int64_t inference_end = esp_timer_get_time();    // 推理结束时间
    ESP_LOGI(TAG, "Inference completed in %lld ms", (inference_end - inference_start) / 1000);
    
    size_t free_mem_after = heap_caps_get_free_size(MALLOC_CAP_SPIRAM);
    ESP_LOGI(TAG, "Free memory after inference: %u bytes", free_mem_after);

    // 获取输出并计算置信度
    auto outputs = model->get_outputs();
    if (outputs.empty()) {
        ESP_LOGE(TAG, "No outputs from model");
    } else {
        // 假设只有一个输出tensor
        auto output_iter = outputs.begin();
        print_confidences(output_iter->second);
    }

    // 清理资源
    delete input_tensor;
    delete model;
    
    ESP_LOGI(TAG, "Gesture recognition completed");
}
