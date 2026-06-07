#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from task3.srv import PrimeFactors
from functools import partial
import sys

class client_node(Node):
    def __init__(self):
        super().__init__("client_node")

    def call_prime_factors_service(self, a):
        client = self.create_client(PrimeFactors, "/prime_factors")

        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for service...")

        request = PrimeFactors.Request()
        request.a = a

        future = client.call_async(request)

        future.add_done_callback(partial(self.callback_prime_factors))
    
    def callback_prime_factors(self, future):
        try:
            response = future.result()
            factors_list = list(response.prime_factors)
            self.get_logger().info(f"Result Received!\nPrimeFactors: {factors_list}")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")
        pass

def main(args = None):
    rclpy.init(args=args)
    input_a = int(sys.argv[1])
    node = client_node()
    node.call_prime_factors_service(input_a)
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

# Write your client implementation here.