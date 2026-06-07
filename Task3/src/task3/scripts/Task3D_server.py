#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from task3.srv import PrimeFactors


class server_node(Node):
    def __init__(self):
        super().__init__("prime_factors_server")
        self.srv = self.create_service(PrimeFactors, 'prime_factors', self.handle_prime_factors)

    def handle_prime_factors(self, request, response):
        a = request.a
        factors = []
        divisor = 2
        while a > 1:
            if a % divisor == 0:
                factors.append(divisor)
                a //= divisor
            else:
                divisor += 1
        self.get_logger().info(f'Prime factors of {request.a} are: {factors}')
        response.prime_factors = factors
        return response

def main(args=None):
    rclpy.init(args=args)
    node = server_node()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
# Write your server implementation here.