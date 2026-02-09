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

difference() {
    // cylinder(41,19,19);
    union() {
        translate([0,0,20]) cube([pcbd + 2.6 + 2.4, pcbw + 2.8 + 2.4, 40], center=true);
        translate([(pcbd + 2.6 + 2.4)/2,(pcbw + 2.8 + 2.4)/2,0]) cylinder(40,3.5,3.5);
        translate([(pcbd + 2.6 + 2.4)/-2,(pcbw + 2.8 + 2.4)/-2,0]) cylinder(40,3.5,3.5);
        translate([(pcbd + 2.6 + 2.4 - 1.4)/-2,(pcbw + 2.8 + 2.4 - 1.4)/2,0]) cylinder(40,1.2,1.2);
        translate([(pcbd + 2.6 + 2.4 - 1.4)/2,(pcbw + 2.8 + 2.4 - 1.4)/-2,0]) cylinder(40,1.2,1.2);
    }
    union() {
        // translate([0,0,1]) cylinder(41,12,12);
        translate([0,0,22]) cube([sd + 0.4, smh + 0.4, 45], center = true);
        translate([0,0,21]) cube([pcbd-4, pcbw + 3, 40], center = true);
        translate([0,0,21]) cube([pcbd+2.8, 6.6, 40], center=true);
        translate([0,0,-1.5-pcbh/4-usbh/4+40]) cube([pcbd+2.8, pcbw+3, 3+pcbh/2+usbh/2], center=true);
        // USB port
        translate([15,0, 40]) cube([30, usbw+0.2, usbh], center=true);
        translate([(pcbd + 2.6 + 2.4)/2,(pcbw + 2.8 + 2.4)/2,2]) cylinder(40,1.2,1.2);
        translate([(pcbd + 2.6 + 2.4)/-2,(pcbw + 2.8 + 2.4)/-2,2]) cylinder(40,1.2,1.2);
    }
}