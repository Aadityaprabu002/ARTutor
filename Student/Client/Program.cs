using System;
using System.Net.Sockets;
using System.Net;
using SocketProgramming.Services;
using System.Text;

namespace Client {
    internal class Program {
        static void Main(string[]? args) {

            Socket clientSocket = new Socket(AddressFamily.InterNetwork
                , SocketType.Dgram,
                ProtocolType.Udp);
            clientSocket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.Broadcast, true);
            clientSocket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, true);
            EndPoint socketEndPoint = (EndPoint) new IPEndPoint(IPAddress.Any, 8080);
            clientSocket.Bind(socketEndPoint);

            byte[]? buffer = new byte[1024 * 5];
       
            while (true) {
                clientSocket.ReceiveFrom(buffer,ref socketEndPoint);
                Console.WriteLine(Encoding.UTF8.GetString(buffer));
                Console.WriteLine("Got from {0}", socketEndPoint.ToString());
                Console.ReadKey();
            }
         
        }
    }
}