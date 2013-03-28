# -*- coding: utf-8 -*-
#    Copyright (C) 2013  Christian Ledermann
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import unittest
from datetime import datetime, date
import json

try:
    from czml import czml
except ImportError:
    import czml

from pygeoif import geometry

class BaseClassesTestCase( unittest.TestCase ):

    def test_DateTimeAware(self):
        dtob = czml._DateTimeAware()
        now = datetime.now()
        today = now.date()
        dtob.epoch = now
        self.assertEqual(dtob.epoch, now.isoformat())
        dtob.epoch = now.isoformat()
        self.assertEqual(dtob.epoch, now.isoformat())
        dtob.epoch = today
        self.assertEqual(dtob.epoch, today.isoformat())
        dtob.epoch = None
        self.assertEqual(dtob.epoch, None)

        dtob.nextTime = now
        self.assertEqual(dtob.nextTime, now.isoformat())
        dtob.nextTime = now.isoformat()
        self.assertEqual(dtob.nextTime, now.isoformat())
        dtob.nextTime = today
        self.assertEqual(dtob.nextTime, today.isoformat())
        dtob.nextTime = 1
        self.assertEqual(dtob.nextTime, 1.0)
        dtob.nextTime = '2'
        self.assertEqual(dtob.nextTime, 2.0)
        dtob.nextTime = None
        self.assertEqual(dtob.nextTime, None)

        dtob.previousTime = now
        self.assertEqual(dtob.previousTime, now.isoformat())
        dtob.previousTime = now.isoformat()
        self.assertEqual(dtob.previousTime, now.isoformat())
        dtob.previousTime = today
        self.assertEqual(dtob.previousTime, today.isoformat())
        dtob.previousTime = 1
        self.assertEqual(dtob.previousTime, 1.0)
        dtob.previousTime = '2'
        self.assertEqual(dtob.previousTime, 2.0)
        dtob.previousTime = None
        self.assertEqual(dtob.previousTime, None)

        jst = '{"nextTime": 2, "previousTime": 1, "epoch": "2013-02-18T00:00:00"}'
        dtob.loads(jst)
        self.assertEqual(dtob.previousTime, 1.0)
        self.assertEqual(dtob.nextTime, 2.0)
        self.assertEqual(dtob.data(), json.loads(jst))


    def test_Coordinates(self):
        coord = czml._Coordinates([0,1])
        self.assertEqual(len(coord.coords), 1)
        self.assertEqual(coord.coords[0].x, 0)
        self.assertEqual(coord.coords[0].y, 1)
        self.assertEqual(coord.coords[0].z, 0)
        self.assertEqual(coord.coords[0].t, None)
        coord = czml._Coordinates([0,1,2])
        self.assertEqual(len(coord.coords), 1)
        self.assertEqual(coord.coords[0].x, 0)
        self.assertEqual(coord.coords[0].y, 1)
        self.assertEqual(coord.coords[0].z, 2)
        self.assertEqual(coord.coords[0].t, None)
        now = datetime.now()
        coord = czml._Coordinates([now, 0,1,2])
        self.assertEqual(len(coord.coords), 1)
        self.assertEqual(coord.coords[0].x, 0)
        self.assertEqual(coord.coords[0].y, 1)
        self.assertEqual(coord.coords[0].z, 2)
        self.assertEqual(coord.coords[0].t, now)
        y2k = datetime(2000,1,1)
        coord = czml._Coordinates([now, 0, 1, 2, y2k, 3, 4, 5])
        self.assertEqual(len(coord.coords), 2)
        self.assertEqual(coord.coords[0].x, 0)
        self.assertEqual(coord.coords[0].y, 1)
        self.assertEqual(coord.coords[0].z, 2)
        self.assertEqual(coord.coords[0].t, now)
        self.assertEqual(coord.coords[1].x, 3)
        self.assertEqual(coord.coords[1].y, 4)
        self.assertEqual(coord.coords[1].z, 5)
        self.assertEqual(coord.coords[1].t, y2k)
        coord = czml._Coordinates([now, 0, 1, 2, 6, 3, 4, 5])
        self.assertEqual(coord.coords[1].t, 6)
        coord = czml._Coordinates([now.isoformat(), 0, 1, 2, '6', 3, 4, 5])
        self.assertEqual(coord.coords[1].t, 6)
        self.assertEqual(coord.coords[0].t, now)
        p = geometry.Point(0, 1)
        coord = czml._Coordinates(p)
        self.assertEqual(coord.coords[0].x, 0)
        self.assertEqual(coord.coords[0].y, 1)
        coord = czml._Coordinates([now, p])
        self.assertEqual(coord.coords[0].x, 0)
        self.assertEqual(coord.coords[0].y, 1)
        self.assertEqual(coord.coords[0].t, now)
        p1 = geometry.Point(0, 1, 2)
        coord = czml._Coordinates([now, p, y2k, p1])
        self.assertEqual(coord.coords[0].x, 0)
        self.assertEqual(coord.coords[0].y, 1)
        self.assertEqual(coord.coords[0].z, 0)
        self.assertEqual(coord.coords[0].t, now)
        self.assertEqual(coord.coords[1].x, 0)
        self.assertEqual(coord.coords[1].y, 1)
        self.assertEqual(coord.coords[1].z, 2)
        self.assertEqual(coord.coords[1].t, y2k)

        self.assertEqual(coord.data(), [now.isoformat(), 0, 1, 0,
                                        y2k.isoformat(), 0, 1, 2])



    def testScale(self):
        pass

    def testColor(self):
        col = czml.Color()
        col.rgba = [0, 255, 127]
        self.assertEqual(col.rgba, [0, 255, 127, 1])
        col.rgba = [0, 255, 127, 55]
        self.assertEqual(col.rgba, [0, 255, 127, 55])
        now = datetime.now()
        col.rgba = [now, 0, 255, 127, 55]
        self.assertEqual(col.rgba, [now.isoformat(), 0, 255, 127, 55])
        y2k = datetime(2000,1,1)
        col.rgba = [now, 0, 255, 127, 55, y2k.isoformat(), 5, 6, 7, 8]
        self.assertEqual(col.rgba, [now.isoformat(), 0, 255, 127, 55,
                                    y2k.isoformat(), 5, 6, 7, 8])
        col.rgba = [1, 0, 255, 127, 55, 2, 5, 6, 7, 8]
        self.assertEqual(col.rgba, [1, 0, 255, 127, 55,
                                    2, 5, 6, 7, 8])
        col.rgbaf = [now, 0, 0.255, 0.127, 0.55, y2k.isoformat(), 0.5, 0.6, 0.7, 0.8]
        self.assertEqual(col.rgbaf, [now.isoformat(), 0.0, 0.255, 0.127, 0.55,
                                    y2k.isoformat(), 0.5, 0.6, 0.7, 0.8])
        col2 = czml.Color()
        col2.loads(col.dumps())
        self.assertEqual(col.data(), col2.data())

class CzmlClassesTestCase( unittest.TestCase ):

    def testPosition(self):
        pos = czml.Position()
        now = datetime.now()
        pos.epoch = now
        coords = [7.0, 0.0, 1.0, 2.0, 6.0, 3.0, 4.0, 5.0]
        pos.cartographicRadians = coords
        self.assertEqual(pos.data()['cartographicRadians'],
            coords)
        js = {'epoch': now.isoformat(), 'cartographicRadians': coords}
        self.assertEqual(pos.data(), js)
        self.assertEqual(pos.dumps(), json.dumps(js))
        pos.cartographicDegrees = coords
        self.assertEqual(pos.data()['cartographicDegrees'],
            coords)
        pos.cartesian = coords
        self.assertEqual(pos.data()['cartesian'],
            coords)
        pos2 = czml.Position()
        pos2.loads(pos.dumps())
        self.assertEqual(pos.data(), pos2.data())


    def testPoint(self):
        point = czml.Point()
        point.color = {'rgba': [0, 255, 127, 55]}
        self.assertEqual(point.data(), {'color':
                {'rgba': [0, 255, 127, 55]},
                'show': False})
        point.outlineColor = {'rgbaf': [0.0, 0.255, 0.127, 0.55]}
        self.assertEqual(point.data(),{'color':
                    {'rgba': [0, 255, 127, 55]},
                    'outlineColor': {'rgbaf': [0.0, 0.255, 0.127, 0.55]},
                    'show': False})
        point.pixelSize = 10
        point.outlineWidth = 2
        point.show = True
        self.assertEqual(point.data(),{'color':
                        {'rgba': [0, 255, 127, 55]},
                    'pixelSize': 10,
                    'outlineColor':
                        {'rgbaf': [0.0, 0.255, 0.127, 0.55]},
                    'outlineWidth': 2,
                    'show': True})
        p2 = czml.Point()
        p2.loads(point.dumps())
        self.assertEqual(point.data(), p2.data())



    def testLabel(self):
        l = czml.Label()
        l.text = 'test label'
        l.show = False
        self.assertEqual(l.data(), {'text': 'test label', 'show': False})
        l.show = True
        self.assertEqual(l.data(), {'text': 'test label', 'show': True})
        l2 = czml.Label()
        l2.loads(l.dumps())
        self.assertEqual(l.data(), l2.data())



    def testBillboard(self):
        bb = czml.Billboard()
        bb.image = 'http://localhost/img.png'
        bb.scale = 0.7
        bb.show = True
        self.assertEqual(bb.data(),
            {'image': 'http://localhost/img.png', 'scale': 0.7, 'show': True})
        #bb.color =
        bb2 = czml.Billboard()
        bb2.loads(bb.dumps())
        self.assertEqual(bb.data(), bb2.data())

    def testCZMLPacket(self):
        p = czml.CZMLPacket(id='abc')
        self.assertEqual(p.dumps(), '{"id": "abc"}')
        bb = czml.Billboard()
        bb.image = 'http://localhost/img.png'
        bb.scale = 0.7
        bb.show = True
        p.billboard = bb
        self.assertEqual(p.data(),
            {'billboard': {'image': 'http://localhost/img.png',
            'scale': 0.7, 'show': True}, 'id': 'abc'})
        p2 = czml.CZMLPacket(id='abc')
        p2.loads(p.dumps())
        self.assertEqual(p.data(), p2.data())
        pos = czml.Position()
        coords = [7.0, 0.0, 1.0, 2.0, 6.0, 3.0, 4.0, 5.0]
        pos.cartesian = coords
        p.position = pos
        l = czml.Label()
        l.text = 'test label'
        l.show = False
        p.label = l
        self.assertEqual(p.data(),
            {'billboard': {'image': 'http://localhost/img.png',
            'scale': 0.7, 'show': True}, 'id': 'abc',
            'label': {'show': False, 'text': 'test label'},
            'position': {'cartesian': [7.0, 0.0, 1.0, 2.0, 6.0, 3.0, 4.0, 5.0]}})
        p2.loads(p.dumps())
        self.assertEqual(p.data(), p2.data())
        p3 = czml.CZMLPacket(id='cde')
        p3.point = {'color':
                    {'rgba': [0, 255, 127, 55]},
                    'show': True}
        self.assertEqual(p3.data(),{'id': 'cde',
                                    'point': {'color':
                                        {'rgba': [0, 255, 127, 55]},
                                        'show': True}})
        return p

    def testCZML(self):
        cz = czml.CZML()
        self.assertEqual(list(cz.data()), [])
        p = self.testCZMLPacket()
        cz.packets.append(p)
        self.assertEqual(list(cz.data()),
            [{'billboard': {'image': 'http://localhost/img.png',
            'scale': 0.7, 'show': True}, 'id': 'abc',
            'label': {'show': False, 'text': 'test label'},
            'position': {'cartesian': [7.0, 0.0, 1.0, 2.0, 6.0, 3.0, 4.0, 5.0]}}])
        cz1 = czml.CZML()
        cz1.loads(cz.dumps())
        self.assertEqual(list(cz.data()),list(cz1.data()))



def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BaseClassesTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()
