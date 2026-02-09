$fn = 120;

pcbh = 1.7;
pcbw = 18.3;
pcbd = 22.9;
sd = 22.3;
dpw = 2.6;
smh = 1.2;
ah = 1.1; // ceramic antenna
aw = 6.2;
usbw = 9.2;
usbh = 3.2;

union() {
    difference() {
        union() {
            translate([-3,-40,0]) cube([6, 40, 3.0]);
            translate([(pcbw + 2.8)/-2,-6,0]) cube([pcbw + 2.8, 9, 3.0]);
            // Clicky thingy
            /* hull() {
                translate([(pcbw + 2.8)/-2,1,3]) cube([pcbw + 2.8, 2, 0.2]);
                translate([(pcbw + 2.8)/-2,2.6,4.4]) cube([pcbw + 2.8, 0.4, 0.2]);
            } */
        }
        // Groove y
        translate([-1.5 + smh/2,-40, 1.2 + (pcbd-sd)/2]) cube([smh + 0.2, 37, 5]);
        // Groove x
        translate([(pcbw + 0.4) / -2, -3 - pcbh/2, 1.2]) cube([pcbw + 0.4, pcbh + 0.2, 5]);
        // Antenna
        translate([aw/-2, -3 + pcbh/2, 1.2]) cube([aw, ah, 5]);
        // USB 
        // translate([usbw/-2, -3 + pcbh/2, 0]) cube([usbw, usbh, 7]);
        // Pin header on USB side
        // translate([pcbw/2 - 2.4 , - 12, 1.2]) cube([2.6, 12, 5]);
        // Pin header opposing side
        translate([pcbw/-2 - 0.2 , - 12, 1.2]) cube([2.6, 12, 5]);
    }
    translate([-3, -35, 1.4 + (pcbd-sd)/2]) rotate([0,90,0]) cylinder(6,1.4,1.4);
}