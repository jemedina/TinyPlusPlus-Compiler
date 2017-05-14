using System;
using System.Collections.Generic;
using System.IO;

public class ConfigurationManager
{

    private const String CONFIG_FILENAME = "conf.json";
    private const String COMPILER_LOCATION_STR = "compilerLocation";
    private Dictionary<String, String> configuration = new Dictionary<String, String>();

    public ConfigurationManager()
    {

    }
    public void loadJsonConfig()
    {
        using (StreamReader jsonReader = new StreamReader(CONFIG_FILENAME))
        {
            string json = jsonReader.ReadToEnd();
            dynamic configItem = JsonConvert.DeserializeObject.DeserializeObject(json);
            foreach (var item in array)
            {
                configuration.put(COMPILER_LOCATION_STR, item.compilerLocation);
            }
        }
    }
}
