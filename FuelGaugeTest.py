import SupplyStatus
import Victron
import mylogging
import Release
import ThreadWatchdog
import FuelGauge

logger = mylogging.Logging()
logger.setLogLevel("DEBUG", "False")

logger.Info("Starting SolarServer")


fuelGauge = FuelGauge.FuelGauge("Battery.xml", logger)




