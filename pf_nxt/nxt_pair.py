import pexpect


class Pair(object):
    def __init__(self, baddr, pin):
        '''
        Pair your device via bluetooth

        :param baddr: The bluetooth mac address
        :param pin: The pin to ensure the connection
        '''

        self._baddr = baddr
        self._pin = pin

        self.pair_device()

    def __del__(self):
        '''
        Removes the paired device and disables the scan if needed.
        Exits bluetoothctl
        '''
        self.clear_bluetooth()
        self.proc.sendline("exit")
        print("Paired nxt removed")

    def clear_bluetooth(self):
        '''
        Just removes the devise and stops the scanning, even if it's not needed. It won't hurt :)
        '''
        self.proc.sendline("remove " + self._baddr)
        self.proc.sendline("scan off")

    def pair_device(self):
        '''
        Pairs the device
        '''
        # TODO: Add a non hardcoded solution (This solution may not work with non english systems)

        print("Pairing with " + self._baddr + "...")
        self.proc = pexpect.spawn('bluetoothctl')

        # Init fixes to make 100% sure that nothing will stop us!! (only works if agent is on)
        self.clear_bluetooth()

        self.proc.sendline("agent on")
        self.proc.expect("Agent registered")
        print(self.proc.after.decode())

        self.proc.sendline("scan on")
        self.proc.expect("Discovery started")
        print(self.proc.after.decode())

        print("Pairing...")
        print("Watch the screen of your robot!")

        # Tries to pairs with bluetooth mac address.
        # If the string "Enter PIN Code" was recognized, break the pairing loop
        for x in range(0, 10):
            try:
                self.proc.sendline("pair " + self._baddr)
                self.proc.expect("Enter PIN code", timeout=2)
                break
            except:
                pass
        else:
            raise Exception("Couldn't connect to bluetooth device, a second try will mostly fix it!")

        self.proc.sendline(self._pin)
        self.proc.expect("Pairing successful")
        print(self.proc.after.decode())

        self.proc.sendline("scan off")
        self.proc.expect("Discovery stopped")
        print(self.proc.after.decode())

        print("Your device is now paired!")
