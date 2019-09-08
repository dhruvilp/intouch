import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

const white = Colors.white;
const grey_light = const Color(0xFFECEFF1);
const off_white = const Color(0xFFfff5e8);
const grey = const Color(0xFF898c8c);
const bluegrey = const Color(0xFF3E5569);
const charcoal_light = const Color(0xFF2f363d);
const charcoal = const Color(0xFF24292E);
const black = Colors.black;
const transparent = const Color(0x263E5569);

//Palette

const cyan_dark = const Color(0xFF114B5F);
const cyan = const Color(0xFF028090);
const off_cyan = const Color(0xFFE4FDE1);
const pink = const Color(0xFFF45B69);

const cyan_gradient = const LinearGradient(
    colors: [cyan, cyan_dark],
    begin: const FractionalOffset(0.4, 0.0),
    end: const FractionalOffset(0.0, 0.5),
    stops:[0.0,1.0],
    tileMode: TileMode.clamp,
);