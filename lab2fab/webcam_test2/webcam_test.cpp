#include <boost/optional.hpp>
#include <string>
#include <vector>
#include <viam/sdk/robot/client.hpp>
#include <viam/sdk/components/camera.hpp>

using namespace viam::sdk;

int main() {
    std::string host("laptop-main.muhvcb3otx.viam.cloud");
    DialOptions dial_opts;
    dial_opts.set_entity(std::string("097504c3-1569-464a-bf81-53805bf93dae")); 
    Credentials credentials("api-key", "20cqh9adz7c6fkiih9ppbr1go0gr41y4");  
    dial_opts.set_credentials(credentials);
    boost::optional<DialOptions> opts(dial_opts);
    Options options(0, opts);

    auto machine = RobotClient::at_address(host, options);

    std::cout << "Resources:\n";
    for (const Name& resource : machine->resource_names()) {
	std::cout << "\t" << resource << "\n";
    }
    
      // Note that the supplied MIME type is just a placeholder. Please update as necessary.
      // webcam
      auto webcam = machine->resource_by_name<Camera>("webcam");
      auto webcam_get_image_return_value = webcam->get_image(std::string("image/png"));
      // note that not all return types are streamable; some conversion may be necessary.
      std::cout << "webcam get_image return value " << webcam_get_image_return_value << "\n";

    return EXIT_SUCCESS;
}

