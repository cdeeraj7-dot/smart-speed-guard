#include <Wire.h>

#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/drivers/i2c.h>

namespace {

constexpr uint8_t kMpuAddress0 = 0x68;
constexpr uint8_t kMpuAddress1 = 0x69;
const struct device *const kI2c3 = DEVICE_DT_GET(DT_NODELABEL(i2c3));

void printAddress(uint8_t address)
{
  Serial.print(F("Address 0x"));
  Serial.println(address, HEX);
}

void probeAddress(uint8_t address)
{
  printAddress(address);

  Wire2.beginTransmission(address);
  const uint8_t wireResult = Wire2.endTransmission();
  Serial.print(F("  Wire2.endTransmission(): "));
  Serial.println(wireResult == 0 ? F("success (0)") : F("error (1; core hides raw error)"));

  const int zephyrResult = i2c_write(kI2c3, nullptr, 0, address);
  Serial.print(F("  Zephyr zero-byte i2c_write(): "));
  Serial.println(zephyrResult);
}

}  // namespace

void setup()
{
  Serial.begin(115200);
  Wire2.begin();
  delay(1000);

  Serial.println(F("MPU6050 I2C address-only probe"));
  Serial.println(F("No registers are read or written; no data bytes are sent."));
  Serial.println(F("A zero-byte transfer error may reflect NACK, bus error, or unsupported probe behavior."));

  Serial.print(F("I2C3 controller ready: "));
  Serial.println(device_is_ready(kI2c3) ? F("YES") : F("NO"));

  if (!device_is_ready(kI2c3)) {
    Serial.println(F("Skipping address probes because I2C3 is not ready."));
    return;
  }

  probeAddress(kMpuAddress0);
  probeAddress(kMpuAddress1);
}

void loop()
{
  delay(1000);
}
