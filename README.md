Author: Jason Edelman
Email: jedelman8@gmail.com

cpal.py is the main module.  It requires other modules such as Cisco, Arista, pandums, jformat, and counter.


If you want to contirubte, you are more than welcome.  There is still a ton to do on the first two module (onePK and eAPI) and it would be great to see more modules.  As more modules evolve, we'll need to update the main cpal.py file to include more variables/function that will in turn call the new modules.

Current plan (for me or you):
- Convert many of the functions in cpal/device variables.  This will make it easier for users to call them
- This is just a module now, but am going to include something in 'main' to be able to call specific functions for specific devices.  Good for helpdesk/admin types that don't need or want to be at the shell
- Adding ODL as a southbound module
- Update names from the vendor like Cisco and Arista.  Will change to cisco-onepk and arista-eapi to allow for more API types from the same vendor.
- Jeremy Schulman also has the Juniper PyEZ module.  It would be great to build cohesiveness or just integrate that here as well.

Things others have talked about:
- Adding NX-API
- Adding F5 APIs

Side note, as more APIs are added, we can get fancier with the function calls correlating data between routers, switches, load balancers, and the like!  This is where it'll get fun.  We'll need to think about this one.


If you want to contribute to an existing module, just let me know before you do.  It'll streamline the integration process.
